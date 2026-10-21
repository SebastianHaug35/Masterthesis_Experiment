"""Normierung von Regelwerk-Namen und Fundstellen (von stufe2.py und evaluate.py genutzt)."""
import re

# Kurzform -> Muster für Kurzform oder vollständigen Titel (Kleinschreibung)
REGELWERK_MUSTER = [
    ("DSGVO", r"\bdsgvo\b|\bds-gvo\b|datenschutz-grundverordnung|2016/679|\bgdpr\b"),
    ("AI Act", r"\bai act\b|\bki-vo\b|ki-verordnung|2024/1689|artificial intelligence act|verordnung über künstliche intelligenz"),
    ("AGG", r"\bagg\b|allgemeines gleichbehandlungsgesetz"),
    ("SGB IX", r"\bsgb ix\b|\bsgb 9\b|neuntes buch sozialgesetzbuch|sozialgesetzbuch neuntes buch"),
    ("GG", r"^gg$|\bgg\b|grundgesetz"),
    ("TV-L", r"\btv-l\b|\btvl\b|tarifvertrag für den öffentlichen dienst der länder"),
    ("NachwG", r"\bnachwg\b|nachweisgesetz"),
    ("BayPVG", r"\bbaypvg\b|bayerisches personalvertretungsgesetz"),
    ("BayGlG", r"\bbayglg\b|bayerisches gleichstellungsgesetz"),
    ("BayDSG", r"\bbaydsg\b|bayerisches datenschutzgesetz"),
    ("WissZeitVG", r"\bwisszeitvg\b|wissenschaftszeitvertragsgesetz|befristete arbeitsverträge in der wissenschaft"),
    ("TzBfG", r"\btzbfg\b|teilzeit- und befristungsgesetz|befristungsgesetz"),
    ("BayHIG", r"\bbayhig\b|hochschulinnovationsgesetz"),
]


def eu_bezeichnung(kurz: str) -> str | None:
    """Kurzform -> 'Verordnung (EU) JJJJ/NNN', sofern das Muster der Kurzform eine EU-Nummer enthält."""
    for k, muster in REGELWERK_MUSTER:
        if k == kurz and (m := re.search(r"(\d{4})/(\d+)", muster)):
            return f"Verordnung (EU) {m.group(1)}/{m.group(2)}"
    return None


def _suche(text: str) -> str | None:
    t = text.lower()
    for kurz, muster in REGELWERK_MUSTER:
        if re.search(muster, t):
            return kurz
    return None


def norm_regelwerk(regelwerk: str, titel: str = "") -> str:
    """Kurzform laut Soll-Liste; unbekannte Regelwerke bleiben (bereinigt) erhalten.
    Bei kombinierten Angaben ('DSGVO / BayDSG') zählt das erste erkannte Regelwerk."""
    return _suche(regelwerk or "") or _suche(titel or "") or " ".join((regelwerk or "").split())


def regelwerke_einzeln(regelwerk: str) -> list[tuple[str, str]]:
    """'DSGVO / BayDSG' -> [('DSGVO', 'DSGVO'), ('BayDSG', 'BayDSG')] als (Rohname, Kurzform)."""
    teile = [t.strip() for t in re.split(r"\s*(?<!\d)/(?!\d)\s*|\s*;\s*|\s*,\s*|(?<!-)\s+und\s+", regelwerk or "") if t.strip()]
    return [(t, norm_regelwerk(t)) for t in teile] or [("", "")]


_ART = re.compile(
    r"(art(?:ikel|t)?\.?|§§?|paragra(?:f|ph)|anhang|annex)\s*"
    r"([0-9]+[a-z]?\b|[ivxlc]+\b)"
    r"((?:\s*(?:,|und|sowie)\s*[0-9]+[a-z]?\b(?!\s*(?:abs|satz|sätze|buchst|nr|lit)))*)",
    re.I)
_ABS_START = re.compile(r"abs(?:atz|ätze)?\.?\s*|^\s*(?=\(\d)", re.I)
_ABS_ENDE = re.compile(r"satz|sätze|buchst|lit\.|\bnr\.|nummer|;|art(?:ikel)?\.?\s*\d|§|anhang|i\.\s*v\.\s*m", re.I)
_NR = re.compile(r"n(?:umme)?r\.?\s*(\d+)", re.I)


def _zahlen(text: str) -> set[str]:
    """'1, 2 und 5' -> {1,2,5}; '1–4' / '1 bis 4' -> {1,2,3,4}; '(11)' -> {11}."""
    werte = set()
    for von, bis in re.findall(r"(\d+[a-z]?)(?:\s*(?:–|-|bis)\s*(\d+))?", text):
        if bis and von.isdigit():
            werte.update(str(i) for i in range(int(von), int(bis) + 1))
        else:
            werte.add(von)
    return werte


def _absaetze(rest: str) -> set[str]:
    absaetze = set()
    for m in _ABS_START.finditer(rest):
        stueck = rest[m.end():]
        ende = _ABS_ENDE.search(stueck)
        absaetze |= _zahlen(stueck[:ende.start()] if ende else stueck)
    return absaetze


def norm_fundstellen(fundstelle: str) -> list[tuple[str, frozenset]]:
    """Alle Normen einer Fundstelle als (Artikel/Paragraf, Absätze).

    'Art.26 Abs.11'                       -> [('Art. 26', {'11'})]
    'Art. 6 Abs. 2 und 3; Anhang III Nr. 4' -> [('Art. 6', {'2','3'}), ('Anhang III', {'4'})]
    '§§ 7, 11'                            -> [('§ 7', {}), ('§ 11', {})]
    Bei Anhängen gilt 'Nr.' als Absatz. Satz/Buchst./Nr. unterhalb des Absatzes werden ignoriert.
    """
    if not fundstelle or not fundstelle.strip():
        return []
    treffer = list(_ART.finditer(fundstelle))
    normen = []
    for i, m in enumerate(treffer):
        rest = fundstelle[m.end(): treffer[i + 1].start() if i + 1 < len(treffer) else len(fundstelle)]
        art_roh = m.group(1).lower()
        nummern = [m.group(2)] + re.findall(r"[0-9]+[a-z]?", m.group(3) or "")
        if art_roh.startswith(("anhang", "annex", "anlage")):
            nr = _NR.search(rest)
            normen.append((f"Anhang {m.group(2).upper()}", frozenset([nr.group(1)] if nr else [])))
            continue
        norm = "§" if art_roh.startswith(("§", "paragra")) else "Art."
        absaetze = frozenset(_absaetze(rest)) if len(nummern) == 1 else frozenset()
        normen += [(f"{norm} {n.lower()}", absaetze) for n in nummern]
    return normen


def norm_fundstelle(fundstelle: str) -> tuple[str | None, str | None]:
    """Erste Norm als ('Art. 26', 'Abs. 11') – für die einfachen Einträge der Soll-Liste."""
    normen = norm_fundstellen(fundstelle)
    if not normen:
        return None, None
    art, absaetze = normen[0]
    if not absaetze:
        return art, None
    praefix = "Nr." if art.startswith("Anhang") else "Abs."
    return art, f"{praefix} {sorted(absaetze)[0]}"


def absatz_nummer(unter: str | None) -> str | None:
    """'Abs. 11' / 'Nr. 4' -> '11' / '4'."""
    return unter.split()[-1] if unter else None


def fundstelle_text(fundstelle: str) -> str:
    normen = norm_fundstellen(fundstelle)
    if not normen:
        return " ".join((fundstelle or "").split())
    teile = []
    for art, absaetze in normen:
        praefix = "Nr." if art.startswith("Anhang") else "Abs."
        nr = "/".join(sorted(absaetze, key=lambda x: (len(x), x)))
        teile.append(f"{art} {praefix} {nr}" if absaetze else art)
    return "; ".join(teile)


def zerlege_fund(regelwerk: str, fundstelle: str) -> list[tuple[str, str | None, frozenset]]:
    """Fund -> Liste (Regelwerk-Kurzform, Artikel/Paragraf, Absätze); ohne erkennbare Norm: [(rw, None, {})].

    Abschnitte (getrennt durch ';') werden dem darin genannten Regelwerk zugeordnet
    ('DSGVO Art. 9; BayDSG Art. 8'), sonst allen Regelwerken des Funds.
    """
    rws = regelwerke_einzeln(regelwerk)
    ergebnis = []
    for abschnitt in re.split(r";", fundstelle or ""):
        normen = norm_fundstellen(abschnitt)
        if not normen:
            continue
        genannt = [kurz for roh, kurz in rws if roh and roh.lower() in abschnitt.lower()]
        if not genannt and (s := _suche(abschnitt)):
            genannt = [s]
        for rw in genannt or [kurz for _, kurz in rws]:
            ergebnis += [(rw, art, abs_) for art, abs_ in normen]
    return ergebnis or [(kurz, None, frozenset()) for _, kurz in rws]
