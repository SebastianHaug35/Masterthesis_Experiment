"""Eigene Recherche-Werkzeuge (Function Calling) für die vier Rechtsquellen, mit lokalem Cache.

    python -m src.werkzeuge --test      # Smoke-Test

Quellen:
- Bund:   gesetze-im-internet.de (Gesamtverzeichnis gii-toc.xml, XML-Download je Gesetz)
- Bayern: gesetze-bayern.de (Suche der Seite, Gesamtansicht /Content/Document/<Abk>/true)
- EU:     eur-lex.europa.eu – Abruf über die Cellar-Schnittstelle des Amts für Veröffentlichungen
          (publications.europa.eu), weil eur-lex.europa.eu Skripte mit einer WAF-Challenge abweist;
          ausgegeben wird die EUR-Lex-URL desselben CELEX-Dokuments (siehe DECISIONS.md, v3)
- Tarif:  tdl-online.de (TV-L als PDF, nach Paragrafen zerlegt)

Im Code steht keine Liste bestimmter Regelwerke; die Auflösung funktioniert für beliebige Regelwerke dieser Quellen.
"""
import argparse
import hashlib
import html
import io
import json
import re
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from http.cookiejar import CookieJar
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
CACHE_DIR = BASIS / "cache"
USER_AGENT = "Masterarbeit-HM-Experiment (nicht-kommerziell)"
MAX_ZEICHEN = 6000
MAX_TREFFER = 10
ERLAUBTE_DOMAINS = {"www.gesetze-im-internet.de", "gesetze-im-internet.de", "www.gesetze-bayern.de",
                    "gesetze-bayern.de", "eur-lex.europa.eu", "publications.europa.eu", "www.tdl-online.de",
                    "tdl-online.de"}

GII = "https://www.gesetze-im-internet.de"
BAY = "https://www.gesetze-bayern.de"
CELLAR = "https://publications.europa.eu"
TDL = "https://www.tdl-online.de"


class NichtGefunden(Exception):
    pass


# --------------------------------------------------------------------------- Abruf mit Cache

class Abruf:
    """HTTP-Abruf: nur erlaubte Domains, höchstens 1 Anfrage/s je Domain, jede Anfrage nur einmal (Cache)."""

    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self._letzte: dict[str, float] = {}
        self._lock = threading.Lock()
        self._domain_locks: dict[str, threading.Lock] = {}
        self.cookies = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))

    def _pfad(self, url: str, schluessel: str) -> Path:
        domain = urllib.parse.urlparse(url).hostname or "unbekannt"
        h = hashlib.sha1(schluessel.encode("utf-8")).hexdigest()[:20]
        return self.cache_dir / domain.removeprefix("www.") / h

    def _warte(self, domain: str) -> threading.Lock:
        with self._lock:
            lock = self._domain_locks.setdefault(domain, threading.Lock())
        return lock

    def hole(self, url: str, *, headers: dict | None = None, daten: dict | None = None,
             cache: bool = True, ok_404: bool = False) -> bytes | None:
        """Liefert den Inhalt (bytes); bei 404 und ok_404 None. Ergebnis wird mit Abrufdatum gecacht."""
        domain = urllib.parse.urlparse(url).hostname or ""
        if domain not in ERLAUBTE_DOMAINS:
            raise PermissionError(f"Domain nicht erlaubt: {domain}")
        schluessel = json.dumps([url, headers or {}, daten or {}], sort_keys=True)
        pfad = self._pfad(url, schluessel)
        if cache and pfad.with_suffix(".meta.json").exists():
            meta = json.loads(pfad.with_suffix(".meta.json").read_text(encoding="utf-8"))
            return None if meta.get("status") == 404 else pfad.with_suffix(".bin").read_bytes()
        kopf = {"User-Agent": USER_AGENT, **(headers or {})}
        body = urllib.parse.urlencode(daten).encode() if daten is not None else None
        with self._warte(domain):
            pause = 1.0 - (time.monotonic() - self._letzte.get(domain, 0))
            if pause > 0:
                time.sleep(pause)
            try:
                req = urllib.request.Request(url, data=body, headers=kopf)
                with self.opener.open(req, timeout=120) as resp:
                    inhalt, status, final = resp.read(), resp.status, resp.geturl()
            except urllib.error.HTTPError as e:
                if e.code == 404 and ok_404:
                    inhalt, status, final = b"", 404, url
                else:
                    raise
            finally:
                self._letzte[domain] = time.monotonic()
        if status == 202 and not inhalt:
            raise RuntimeError(f"Abruf blockiert (HTTP 202 ohne Inhalt, WAF-Challenge): {url}")
        if cache:
            pfad.parent.mkdir(parents=True, exist_ok=True)
            pfad.with_suffix(".bin").write_bytes(inhalt)
            pfad.with_suffix(".meta.json").write_text(json.dumps(
                {"url": url, "final_url": final, "status": status, "headers": headers or {}, "daten": daten or {},
                 "abgerufen": datetime.now().astimezone().isoformat(timespec="seconds")},
                ensure_ascii=False, indent=1), encoding="utf-8")
        return None if status == 404 else inhalt


# --------------------------------------------------------------------------- Datenmodell

@dataclass
class Norm:
    norm: str            # Anzeigeform, z. B. "Art. 35", "§ 165", "Anhang III"
    ueberschrift: str
    text: str
    quelle_url: str


@dataclass
class Dokument:
    kennung: str         # eindeutige Kennung, z. B. "bund:agg", "bayern:BayPVG", "eu:32016R0679", "tarif:TV-L"
    regelwerk: str       # Abkürzung bzw. Kurzbezeichnung
    titel: str
    ebene: str
    quelle_url: str
    fassung_datum: str
    normen: dict[str, Norm] = field(default_factory=dict)   # Schlüssel: norm_schluessel()


_ROEMISCH = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}


def _roemisch(s: str) -> int | None:
    s = s.lower()
    if not s or any(c not in _ROEMISCH for c in s):
        return None
    wert = 0
    for i, c in enumerate(s):
        v = _ROEMISCH[c]
        wert += -v if i + 1 < len(s) and _ROEMISCH[s[i + 1]] > v else v
    return wert


def norm_schluessel(norm: str) -> str | None:
    """'Art. 26 Abs. 11' -> 'art 26'; '§§ 165' -> '§ 165'; 'Anhang III Nr. 4' -> 'anhang iii';
    'Artikel 35' -> 'art 35'; 'Anlage 1' -> 'anlage 1'."""
    t = unicodedata.normalize("NFKC", norm or "").replace("\xa0", " ").strip()
    m = re.match(r"(?i)\s*(§§?|art(?:ikel|\.)?|anhang|annex|anlage)\s*([0-9]+[a-z]?\b|[ivxlc]+\b|[a-z]\b)", t)
    if not m:
        return None
    art = m.group(1).lower()
    nr = m.group(2).lower()
    if art.startswith("§"):
        return f"§ {nr}"
    if art.startswith("art"):
        return f"art {nr}"
    if art in ("anhang", "annex"):
        return f"anhang {nr}"
    return f"anlage {nr}"


def _text(s: str) -> str:
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", s.replace("\xa0", " "))).strip()


def _kuerze(obj: dict) -> str:
    """JSON-Rückgabe auf höchstens MAX_ZEICHEN Zeichen; bei Kürzung 'gekuerzt': true."""
    s = json.dumps(obj, ensure_ascii=False)
    if len(s) <= MAX_ZEICHEN:
        return s
    obj = {**obj, "gekuerzt": True}
    for feld in ("text", "eintraege", "treffer"):
        if feld in obj:
            wert = obj[feld]
            while len(json.dumps(obj, ensure_ascii=False)) > MAX_ZEICHEN:
                if isinstance(wert, str):
                    wert = wert[: max(0, len(wert) - max(200, len(json.dumps(obj, ensure_ascii=False)) - MAX_ZEICHEN))]
                elif wert:
                    wert = wert[:-max(1, len(wert) // 10)]
                else:
                    break
                obj[feld] = wert
    return json.dumps(obj, ensure_ascii=False)[:MAX_ZEICHEN]


# --------------------------------------------------------------------------- Bund

class Bund:
    def __init__(self, abruf: Abruf):
        self.abruf = abruf
        self._toc: list[tuple[str, str]] | None = None   # (slug, titel)

    def toc(self) -> list[tuple[str, str]]:
        if self._toc is None:
            root = ET.fromstring(self.abruf.hole(f"{GII}/gii-toc.xml"))
            self._toc = []
            for item in root.iter("item"):
                link = item.findtext("link") or ""
                m = re.search(r"gesetze-im-internet\.de/([^/]+)/xml\.zip", link)
                if m:
                    self._toc.append((m.group(1), html.unescape(item.findtext("title") or "")))
        return self._toc

    @staticmethod
    def slug_form(abk: str) -> str:
        """'SGB IX' -> 'sgb_9', 'TzBfG' -> 'tzbfg'."""
        teile = []
        for t in re.split(r"\s+", abk.strip()):
            r = _roemisch(t)
            teile.append(str(r) if r and len(t) > 0 and t.isupper() else t.lower())
        return "_".join(teile).replace("-", "_").replace(".", "")

    def finde_slug(self, abk: str) -> str | None:
        form = self.slug_form(abk)
        slugs = [s for s, _ in self.toc()]
        if form in slugs:
            return form
        varianten = sorted((s for s in slugs if re.fullmatch(re.escape(form) + r"_\d{4}", s)), reverse=True)
        return varianten[0] if varianten else None

    def suche(self, stichwort: str) -> list[dict]:
        form = self.slug_form(stichwort)
        woerter = [w.lower() for w in re.findall(r"\w+", stichwort) if len(w) > 2]
        treffer = []
        for slug, titel in self.toc():
            t = titel.lower()
            if slug == form or re.fullmatch(re.escape(form) + r"_\d{4}", slug) or (woerter and all(w in t for w in woerter)):
                treffer.append({"regelwerk": slug, "titel": titel, "ebene": "Bund",
                                "quelle_url": f"{GII}/{slug}/"})
        treffer.sort(key=lambda x: (x["regelwerk"] != form, len(x["titel"])))
        return treffer

    def lade(self, slug: str) -> Dokument:
        z = zipfile.ZipFile(io.BytesIO(self.abruf.hole(f"{GII}/{slug}/xml.zip")))
        root = ET.fromstring(z.read([n for n in z.namelist() if n.endswith(".xml")][0]))
        abk, titel, fassung = slug, slug, ""
        normen: dict[str, Norm] = {}
        for i, n in enumerate(root.iter("norm")):
            md = n.find("metadaten")
            if md is None:
                continue
            if i == 0:
                abk = md.findtext("jurabk") or md.findtext("amtabk") or slug
                titel = _text("".join(md.find("langue").itertext())) if md.find("langue") is not None else abk
                stand = [_text(" ".join(s.itertext())) for s in md.iter("standangabe")]
                fassung = "; ".join(stand) or f"Stand {root.get('builddate', '')[:8]}"
            enbez = (md.findtext("enbez") or "").strip()
            key = norm_schluessel(enbez)
            if not key or key in normen:
                continue
            td = n.find("textdaten")
            text = _text("\n".join(t for t in td.itertext())) if td is not None else ""
            anzeige = enbez.replace("Art ", "Art. ") if enbez.startswith("Art ") else enbez
            datei = (f"__{key.split()[1]}.html" if key.startswith("§") else
                     f"art_{key.split()[1]}.html" if key.startswith("art") else "index.html")
            normen[key] = Norm(anzeige, _text(md.findtext("titel") or ""), text, f"{GII}/{slug}/{datei}")
        return Dokument(f"bund:{slug}", abk, titel, "Bund", f"{GII}/{slug}/", fassung, normen)


# --------------------------------------------------------------------------- Bayern

class Bayern:
    def __init__(self, abruf: Abruf):
        self.abruf = abruf

    def existiert(self, abk: str) -> bool:
        if not re.fullmatch(r"[A-Za-zÄÖÜäöüß0-9_]+", abk or ""):
            return False
        inhalt = self.abruf.hole(f"{BAY}/Content/Document/{abk}", ok_404=True)
        return bool(inhalt) and f"({abk})" in inhalt.decode("utf-8", "replace")

    def suche(self, stichwort: str) -> list[dict]:
        """Suchfunktion der Seite (Formular mit Token), gefiltert auf Gesetze/Verordnungen; dedupliziert nach Abkürzung."""
        treffer: dict[str, dict] = {}
        for filter_ in ("/Search/Filter/NORMTYP/ges", "/Search/Filter/DOKTYP/norm"):
            seite = self._suche_seite(stichwort, filter_)
            for m in re.finditer(r'<a[^>]*href="/Content/Document/([^"?]+)\?hl=true"[^>]*>(.*?)</a>', seite, re.S):
                dok_id, text = m.group(1), _text(html.unescape(re.sub(r"<[^>]+>", " ", m.group(2))))
                abk = dok_id.split("-")[0]
                if abk.startswith(("BayVV", "Y-")) or abk in treffer:
                    continue
                titel = re.sub(r"\s+–.*$", "", text)
                treffer[abk] = {"regelwerk": abk, "titel": titel, "ebene": "Land",
                                "quelle_url": f"{BAY}/Content/Document/{abk}"}
            if len(treffer) >= MAX_TREFFER:
                break
        return list(treffer.values())

    def _suche_seite(self, stichwort: str, filter_: str) -> str:
        schluessel_url = f"{BAY}{filter_}?q={urllib.parse.quote(stichwort)}"
        pfad = self.abruf._pfad(schluessel_url, schluessel_url)
        if pfad.with_suffix(".bin").exists():
            return pfad.with_suffix(".bin").read_text(encoding="utf-8")
        start = self.abruf.hole(f"{BAY}/Search", cache=False).decode("utf-8", "replace")
        token = re.search(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"', start)
        self.abruf.hole(f"{BAY}/Search", daten={"__RequestVerificationToken": token.group(1) if token else "",
                                               "SearchFields.Content": stichwort}, cache=False)
        seite = self.abruf.hole(f"{BAY}{filter_}", cache=False).decode("utf-8", "replace")
        pfad.parent.mkdir(parents=True, exist_ok=True)
        pfad.with_suffix(".bin").write_text(seite, encoding="utf-8")
        pfad.with_suffix(".meta.json").write_text(json.dumps(
            {"url": schluessel_url, "status": 200, "abgerufen": datetime.now().astimezone().isoformat(timespec="seconds")},
            ensure_ascii=False), encoding="utf-8")
        return seite

    def lade(self, abk: str) -> Dokument:
        seite = self.abruf.hole(f"{BAY}/Content/Document/{abk}/true", ok_404=True)
        if not seite:
            raise NichtGefunden(abk)
        s = seite.decode("utf-8", "replace")
        import lxml.html
        root = lxml.html.fromstring(s)
        titel = _text(root.findtext(".//title") or abk).split(" - ")[0]
        titel = re.sub(rf"^{re.escape(abk)}:\s*", "", titel)
        gilt = re.search(r"Text gilt ab:\s*([0-9.]+)", _text(root.text_content()))
        fassung = f"Text gilt ab {gilt.group(1)}" if gilt else ""
        normen: dict[str, Norm] = {}
        for cont in root.xpath('//div[@class="cont"]'):
            nr = cont.xpath('.//div[contains(@class,"paranr")]')
            if not nr:
                continue
            anzeige = _text(nr[0].text_content())
            key = norm_schluessel(anzeige)
            if not key or key in normen:
                continue
            ueb = cont.xpath('.//div[contains(@class,"paratitel")]')
            text = "\n".join(_text(p.text_content()) for p in cont.xpath('.//div[contains(@class,"paratext")]'))
            nummer = key.split()[1]
            normen[key] = Norm(anzeige, _text(ueb[0].text_content()) if ueb else "", text,
                               f"{BAY}/Content/Document/{abk}-{nummer}")
        return Dokument(f"bayern:{abk}", abk, titel, "Land", f"{BAY}/Content/Document/{abk}", fassung, normen)


# --------------------------------------------------------------------------- EU

class EU:
    SPARQL = f"{CELLAR}/webapi/rdf/sparql"

    def __init__(self, abruf: Abruf):
        self.abruf = abruf

    @staticmethod
    def celex_aus_text(text: str) -> str | None:
        """'Verordnung (EU) 2016/679' -> '32016R0679'; 'Richtlinie (EU) 2019/1152' -> '32019L1152';
        'CELEX:32016R0679' -> '32016R0679'."""
        m = re.search(r"celex[:\s]*([0-9]{5}[A-Z][0-9]{4})", text, re.I)
        if m:
            return m.group(1).upper()
        m = re.search(r"(\d{4})/(\d{1,4})(?!\d)", text)
        if not m:
            return None
        art = "L" if re.search(r"richtlinie|directive|\bRL\b", text, re.I) else "R"
        return f"3{m.group(1)}{art}{int(m.group(2)):04d}"

    def _sparql(self, query: str) -> list[dict]:
        roh = self.abruf.hole(f"{self.SPARQL}?{urllib.parse.urlencode({'query': query})}",
                              headers={"Accept": "application/sparql-results+json"})
        return [{k: v["value"] for k, v in b.items()} for b in json.loads(roh)["results"]["bindings"]]

    def suche(self, stichwort: str) -> list[dict]:
        treffer = []
        celex = self.celex_aus_text(stichwort)
        woerter = [w.lower() for w in re.findall(r"[\wäöüß-]+", stichwort) if len(w) > 2]
        if celex:
            bedingung = f'FILTER(STR(?celex) = "{celex}")'
        elif woerter:
            bedingung = " ".join(f'FILTER(CONTAINS(LCASE(STR(?title)), "{w.replace(chr(34), "")}"))' for w in woerter)
        else:
            return []
        q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
SELECT DISTINCT ?celex ?title WHERE {{
  ?w cdm:resource_legal_id_celex ?celex .
  ?e cdm:expression_belongs_to_work ?w ;
     cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/DEU> ;
     cdm:expression_title ?title .
  FILTER(REGEX(STR(?celex), "^3[0-9]{{4}}[RL][0-9]{{4}}$"))
  {bedingung}
}} LIMIT 20"""
        for b in self._sparql(q):
            treffer.append({"regelwerk": self.bezeichnung(b["celex"]), "titel": _text(b["title"]), "ebene": "EU",
                            "quelle_url": f"https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:{b['celex']}"})
        # Stichwort im Kurztitel in Klammern zuerst, Grundrechtsakte vor Änderungs-/Durchführungsakten
        def im_kurztitel(t):
            return any(all(w in k.lower() for w in woerter) for k in re.findall(r"\(([^()]+)\)", t["titel"]))
        treffer.sort(key=lambda t: (not im_kurztitel(t),
                                    t["titel"].lower().startswith(("berichtigung", "durchführungs", "delegierte")),
                                    "zur änderung" in t["titel"].lower()[:200], len(t["titel"])))
        return treffer

    @staticmethod
    def bezeichnung(celex: str) -> str:
        art = {"R": "Verordnung", "L": "Richtlinie"}.get(celex[5], "Rechtsakt")
        return f"{art} (EU) {celex[1:5]}/{int(celex[6:])}"

    def konsolidiert(self, celex: str) -> str | None:
        q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
SELECT ?celex WHERE {{ ?w cdm:resource_legal_id_celex ?celex .
  FILTER(STRSTARTS(STR(?celex), "0{celex[1:]}-")) }} ORDER BY DESC(?celex) LIMIT 1"""
        r = self._sparql(q)
        return r[0]["celex"] if r else None

    def lade(self, celex: str) -> Dokument:
        import lxml.html
        kons = self.konsolidiert(celex)
        quelle = kons or celex
        roh = self.abruf.hole(f"{CELLAR}/resource/celex/{quelle}", ok_404=True,
                              headers={"Accept": "application/xhtml+xml", "Accept-Language": "deu"})
        if not roh:
            raise NichtGefunden(celex)
        root = lxml.html.fromstring(roh)
        titel_el = root.xpath('//*[contains(@class,"title-doc-first") or contains(@class,"oj-doc-ti") '
                              'or contains(@class,"eli-main-title")]')
        titel = _text(" ".join(e.text_content() for e in titel_el[:3])) or self.bezeichnung(celex)
        if kons:
            d = kons.split("-")[1]
            fassung = f"konsolidierte Fassung vom {d[6:8]}.{d[4:6]}.{d[:4]}"
        else:
            fassung = "Fassung des Amtsblatts (keine konsolidierte Fassung)"
        url = f"https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:{quelle}"
        normen: dict[str, Norm] = {}
        for el in root.xpath('//*[@id]'):
            m = re.fullmatch(r"(art|anx)_([0-9]+[a-z]?|[IVXLC]+)", el.get("id"))
            if not m:
                continue
            key = f"art {m.group(2).lower()}" if m.group(1) == "art" else f"anhang {m.group(2).lower()}"
            if key in normen:
                continue
            tit = root.xpath(f'//*[@id="{el.get("id")}.tit_1"]')
            text = _text(el.text_content())
            ueb = _text(tit[0].text_content()) if tit else ""
            if not ueb and key.startswith("anhang"):
                zeilen = [z for z in text.split("\n") if z.strip()]
                ueb = zeilen[1] if len(zeilen) > 1 else ""
            anzeige = f"Art. {m.group(2)}" if m.group(1) == "art" else f"Anhang {m.group(2)}"
            normen[key] = Norm(anzeige, ueb, text, f"{url}#{el.get('id')}")
        return Dokument(f"eu:{celex}", self.bezeichnung(celex), titel, "EU", url, fassung, normen)


# --------------------------------------------------------------------------- Tarif (TV-L)

class Tarif:
    MUSTER_TVL = re.compile(r"^\s*tv-?l\s*$|tarifvertrag\s+für\s+den\s+öffentlichen\s+dienst\s+der\s+länder", re.I)

    def __init__(self, abruf: Abruf):
        self.abruf = abruf

    def ist_tvl(self, text: str) -> bool:
        return bool(self.MUSTER_TVL.search(text or ""))

    @staticmethod
    def ist_tarifvertrag(text: str) -> bool:
        return bool(re.search(r"^\s*tv[\s-]|tarifvertrag", text or "", re.I))

    def suche(self, stichwort: str) -> list[dict]:
        if self.ist_tvl(stichwort) or re.search(r"tarif|tv-l|länder", stichwort, re.I):
            return [{"regelwerk": "TV-L", "titel": "Tarifvertrag für den öffentlichen Dienst der Länder (TV-L)",
                     "ebene": "Tarif", "quelle_url": f"{TDL}/tarifvertraege/tv-l"}]
        return []

    def lade(self) -> Dokument:
        import pypdf
        seite = self.abruf.hole(f"{TDL}/tarifvertraege/tv-l").decode("utf-8", "replace")
        links = re.findall(r'href="(/fileadmin/[^"]*TV-L__i\.d\.F\.[^"]*\.pdf)"', seite)
        if not links:
            raise NichtGefunden("TV-L-PDF nicht auf tdl-online.de gefunden")
        url = TDL + links[0]
        text = "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(io.BytesIO(self.abruf.hole(url))).pages)
        fassung_m = re.search(r"in der Fassung des Änderungstarifvertrages Nr\.\s*(\d+)\s*vom\s*([^\n]+)", text)
        fassung = f"i. d. F. des ÄTV Nr. {fassung_m.group(1)} vom {fassung_m.group(2).strip()}" if fassung_m else ""
        zeilen = text.split("\n")
        normen: dict[str, Norm] = {}
        aktuell, ueb, puffer = None, "", []

        def ablegen():
            if aktuell and aktuell not in normen:
                normen[aktuell] = Norm(f"§ {aktuell.split()[1]}", ueb, _text("\n".join(puffer)), url)

        for i, z in enumerate(zeilen):
            m = re.fullmatch(r"\s*§\s*(\d+[a-z]?)\s*", z)
            if m:
                ablegen()
                aktuell, puffer = f"§ {m.group(1)}", []
                folgende = [x.strip() for x in zeilen[i + 1:i + 4] if x.strip()]
                ueb = folgende[0] if folgende else ""
                continue
            if aktuell and not re.fullmatch(r"\s*\d{1,3}\s*", z):
                puffer.append(z)
        ablegen()
        return Dokument("tarif:TV-L", "TV-L", "Tarifvertrag für den öffentlichen Dienst der Länder (TV-L)",
                        "Tarif", url, fassung, normen)


# --------------------------------------------------------------------------- Werkzeuge

class Werkzeuge:
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.abruf = Abruf(cache_dir)
        self.bund, self.bayern, self.eu, self.tarif = Bund(self.abruf), Bayern(self.abruf), EU(self.abruf), Tarif(self.abruf)
        self._doks: dict[str, Dokument] = {}
        self._kennungen: dict[str, str | None] = {}
        self._lock = threading.Lock()

    # Auflösung ---------------------------------------------------------------
    def kennung(self, regelwerk: str) -> str | None:
        """Regelwerk-Angabe -> Kennung (bund:/bayern:/eu:/tarif:) oder None."""
        r = " ".join((regelwerk or "").split())
        if not r:
            return None
        with self._lock:
            if r in self._kennungen:
                return self._kennungen[r]
        k = self._kennung(r)
        with self._lock:
            self._kennungen[r] = k
        return k

    def _kennung(self, r: str) -> str | None:
        if re.match(r"(bund|bayern|eu|tarif):", r):
            return r
        celex = self.eu.celex_aus_text(r)
        if celex and (re.search(r"verordnung|richtlinie|\(eu\)|\(eg\)|celex|regulation|directive", r, re.I)):
            return f"eu:{celex}"
        if self.tarif.ist_tvl(r):
            return "tarif:TV-L"
        if self.tarif.ist_tarifvertrag(r):
            return None
        abk = re.sub(r"\s*\(.*?\)\s*$", "", r)
        klammer = re.search(r"\(([^()]+)\)\s*$", r)
        kandidaten = [abk] + ([klammer.group(1)] if klammer else [])
        for a in kandidaten:
            slug = self.bund.finde_slug(a)
            if slug:
                return f"bund:{slug}"
        for a in kandidaten:
            if self.bayern.existiert(a.replace(" ", "")):
                return f"bayern:{a.replace(' ', '')}"
        bund = self.bund.suche(r)
        if bund:
            return f"bund:{bund[0]['regelwerk']}"
        eu = self.eu.suche(r) if len(r) > 3 else []
        if eu:
            return f"eu:{self.eu.celex_aus_text('CELEX:' + eu[0]['quelle_url'].split('CELEX:')[1])}"
        return None

    def dokument(self, kennung: str) -> Dokument:
        with self._lock:
            if kennung in self._doks:
                return self._doks[kennung]
        quelle, _, wert = kennung.partition(":")
        dok = {"bund": lambda: self.bund.lade(wert), "bayern": lambda: self.bayern.lade(wert),
               "eu": lambda: self.eu.lade(wert), "tarif": lambda: self.tarif.lade()}[quelle]()
        with self._lock:
            self._doks[kennung] = dok
        return dok

    def finde_norm(self, regelwerk: str, norm: str) -> tuple[Dokument | None, Norm | None, str | None]:
        """(Dokument, Norm, Norm-Schlüssel); Dokument None = Regelwerk unbekannt, Norm None = nicht im Regelwerk."""
        k = self.kennung(regelwerk)
        if not k:
            return None, None, norm_schluessel(norm)
        try:
            dok = self.dokument(k)
        except NichtGefunden:
            return None, None, norm_schluessel(norm)
        key = norm_schluessel(norm)
        return dok, dok.normen.get(key) if key else None, key

    # Funktionen für das Modell -------------------------------------------------
    def suche_regelwerk(self, stichwort: str) -> dict:
        treffer, gesehen = [], set()
        for quelle in (self.tarif.suche, self.bund.suche, self.eu.suche, self.bayern.suche):
            try:
                ergebnisse = quelle(stichwort)
            except Exception as e:  # eine Quelle darf ausfallen, ohne die anderen zu blockieren
                ergebnisse = [{"fehler": f"{type(e).__name__}: {e}"[:200]}]
            for t in ergebnisse[:4]:
                schluessel = t.get("regelwerk") or json.dumps(t)
                if schluessel not in gesehen:
                    gesehen.add(schluessel)
                    treffer.append(t)
        return {"stichwort": stichwort, "treffer": treffer[:MAX_TREFFER],
                **({} if treffer else {"fehler": "nicht gefunden"})}

    def inhaltsverzeichnis(self, regelwerk: str) -> dict:
        k = self.kennung(regelwerk)
        if not k:
            return {"regelwerk": regelwerk, "fehler": "nicht gefunden"}
        try:
            dok = self.dokument(k)
        except NichtGefunden:
            return {"regelwerk": regelwerk, "fehler": "nicht gefunden"}
        return {"regelwerk": dok.regelwerk, "titel": dok.titel, "quelle_url": dok.quelle_url,
                "fassung_datum": dok.fassung_datum,
                "eintraege": [{"norm": n.norm, "ueberschrift": n.ueberschrift[:80]} for n in dok.normen.values()]}

    def lade_norm(self, regelwerk: str, norm: str) -> dict:
        dok, n, _ = self.finde_norm(regelwerk, norm)
        if dok is None:
            return {"regelwerk": regelwerk, "norm": norm, "fehler": "nicht gefunden",
                    "hinweis": "Regelwerk nicht auflösbar; suche_regelwerk verwenden, EU-Rechtsakte als 'Verordnung (EU) JJJJ/NNNN' angeben"}
        if n is None:
            return {"regelwerk": dok.regelwerk, "norm": norm, "fehler": "nicht gefunden",
                    "hinweis": "Norm nicht in diesem Regelwerk; inhaltsverzeichnis verwenden"}
        return {"regelwerk": dok.regelwerk, "norm": n.norm, "ueberschrift": n.ueberschrift, "text": n.text,
                "quelle_url": n.quelle_url, "fassung_datum": dok.fassung_datum}

    def suche_volltext(self, regelwerk: str, begriff: str) -> dict:
        k = self.kennung(regelwerk)
        if not k:
            return {"regelwerk": regelwerk, "fehler": "nicht gefunden"}
        try:
            dok = self.dokument(k)
        except NichtGefunden:
            return {"regelwerk": regelwerk, "fehler": "nicht gefunden"}
        b = (begriff or "").lower().strip()
        treffer = []
        for n in dok.normen.values():
            i = n.text.lower().find(b) if b else -1
            if i < 0 and b and b in n.ueberschrift.lower():
                i = 0
            if i >= 0:
                start = max(0, i - 120)
                treffer.append({"norm": n.norm, "auszug": n.text[start:start + 300]})
            if len(treffer) >= MAX_TREFFER:
                break
        return {"regelwerk": dok.regelwerk, "begriff": begriff, "treffer": treffer,
                **({} if treffer else {"fehler": "nicht gefunden"})}

    # Dispatcher ------------------------------------------------------------------
    def ausfuehren(self, name: str, argumente: dict) -> tuple[str, dict]:
        """Führt ein Werkzeug aus -> (JSON-Text für das Modell, Protokolleintrag)."""
        start = time.monotonic()
        try:
            ergebnis = getattr(self, name)(**argumente) if name in FUNKTIONEN else {"fehler": f"unbekanntes Werkzeug {name}"}
        except Exception as e:
            ergebnis = {"fehler": f"technischer Fehler: {type(e).__name__}: {e}"[:300]}
        text = _kuerze(ergebnis)
        protokoll = {"funktion": name, "parameter": argumente, "gefunden": "fehler" not in ergebnis,
                     "quelle_url": ergebnis.get("quelle_url"), "gekuerzt": len(json.dumps(ergebnis, ensure_ascii=False)) > MAX_ZEICHEN,
                     "dauer_s": round(time.monotonic() - start, 2)}
        if name == "lade_norm" and "fehler" not in ergebnis:
            protokoll["kennung"] = self.kennung(argumente.get("regelwerk", ""))
            protokoll["norm_schluessel"] = norm_schluessel(argumente.get("norm", ""))
        if "fehler" in ergebnis:
            protokoll["fehler"] = ergebnis["fehler"]
        return text, protokoll


def _schema(props: dict) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


FUNKTIONEN = {
    "suche_regelwerk": ("Sucht Regelwerke (Gesetze, Verordnungen, EU-Rechtsakte, TV-L) in den vier Quellen nach "
                        "Stichwort, Abkürzung oder Titel. EU-Rechtsakte am besten als 'Verordnung (EU) JJJJ/NNNN' "
                        "oder mit Wörtern aus dem amtlichen Titel suchen.",
                        _schema({"stichwort": {"type": "string"}})),
    "inhaltsverzeichnis": ("Liste aller Artikel/Paragrafen/Anhänge eines Regelwerks mit Überschrift.",
                           _schema({"regelwerk": {"type": "string",
                                                  "description": "Abkürzung (z. B. wie von suche_regelwerk geliefert) "
                                                                 "oder 'Verordnung (EU) JJJJ/NNNN'"}})),
    "lade_norm": ("Lädt den Wortlaut einer Norm mit quelle_url und fassung_datum.",
                  _schema({"regelwerk": {"type": "string",
                                         "description": "Abkürzung oder 'Verordnung (EU) JJJJ/NNNN'"},
                           "norm": {"type": "string", "description": "z. B. 'Art. 78', '§ 165', 'Anhang III'"}})),
    "suche_volltext": ("Sucht einen Begriff im Wortlaut eines Regelwerks; liefert bis zu 10 Normen mit Auszug.",
                       _schema({"regelwerk": {"type": "string"}, "begriff": {"type": "string"}})),
}


def tool_definitionen() -> list[dict]:
    return [{"type": "function", "name": n, "description": d, "parameters": p, "strict": True}
            for n, (d, p) in FUNKTIONEN.items()]


# --------------------------------------------------------------------------- Smoke-Test

def smoke_test() -> bool:
    w = Werkzeuge()
    ok = True

    def pruefe(bedingung: bool, text: str):
        nonlocal ok
        ok &= bedingung
        print(("OK    " if bedingung else "FEHLER"), text, flush=True)

    for rw, norm in [("AGG", "§ 7"), ("SGB IX", "§ 165"), ("BayPVG", "Art. 78"), ("BayGlG", "Art. 17"),
                     ("Verordnung (EU) 2016/679", "Art. 35"), ("Verordnung (EU) 2024/1689", "Art. 26"),
                     ("Verordnung (EU) 2024/1689", "Anhang III"), ("TV-L", "§ 12")]:
        r = w.lade_norm(rw, norm)
        pruefe("fehler" not in r and len(r.get("text", "")) > 50,
               f"lade_norm {rw} {norm}: {r.get('ueberschrift', r.get('fehler'))} | {r.get('fassung_datum', '')} | {r.get('quelle_url', '')}")
    for rw, norm in [("DSGVO", "Art. 150"), ("Verordnung (EU) 2016/679", "Art. 150"), ("AGG", "§ 99")]:
        r = w.lade_norm(rw, norm)
        pruefe(r.get("fehler") == "nicht gefunden", f"lade_norm {rw} {norm} -> nicht gefunden ({r.get('hinweis', '')})")
    r = w.suche_regelwerk("Personalvertretung Bayern")
    pruefe(any(t.get("regelwerk") == "BayPVG" for t in r["treffer"]),
           "suche_regelwerk('Personalvertretung Bayern') -> " + ", ".join(t.get("regelwerk", "?") for t in r["treffer"]))
    print("Smoke-Test bestanden" if ok else "Smoke-Test NICHT bestanden")
    return ok


def main() -> None:
    p = argparse.ArgumentParser(description="Recherche-Werkzeuge (H1 v3)")
    p.add_argument("--test", action="store_true", help="Smoke-Test ausführen")
    p.add_argument("--aufruf", nargs=2, metavar=("FUNKTION", "JSON"), help="ein Werkzeug manuell aufrufen")
    a = p.parse_args()
    if a.test:
        raise SystemExit(0 if smoke_test() else 1)
    if a.aufruf:
        text, prot = Werkzeuge().ausfuehren(a.aufruf[0], json.loads(a.aufruf[1]))
        print(text)
        print(prot)


if __name__ == "__main__":
    main()
