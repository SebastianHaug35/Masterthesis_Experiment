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
]


def _suche(text: str) -> str | None:
    t = text.lower()
    for kurz, muster in REGELWERK_MUSTER:
        if re.search(muster, t):
            return kurz
    return None


def norm_regelwerk(regelwerk: str, titel: str = "") -> str:
    """Kurzform laut Soll-Liste; unbekannte Regelwerke bleiben (bereinigt) erhalten."""
    return _suche(regelwerk or "") or _suche(titel or "") or " ".join((regelwerk or "").split())


_ART = re.compile(r"(art(?:ikel)?\.?|§+|paragra(?:f|ph)|anhang|annex)\s*([0-9]+[a-z]?\b|[ivxlc]+\b)", re.I)
_ABS = re.compile(r"abs(?:atz)?\.?\s*(\d+[a-z]?)|^\s*\((\d+[a-z]?)\)", re.I)
_NR = re.compile(r"n(?:umme)?r\.?\s*(\d+)", re.I)


def norm_fundstelle(fundstelle: str) -> tuple[str | None, str | None]:
    """'Art.26 Abs.11' -> ('Art. 26', 'Abs. 11'); 'Anhang III Nr. 4' -> ('Anhang III', 'Nr. 4').

    Bei Aufzählungen (§§ 164, 165 / Art. 44 ff.) zählt die erste Norm. Ohne erkennbare Norm: (None, None).
    """
    if not fundstelle or not fundstelle.strip():
        return None, None
    m = _ART.search(fundstelle)
    if not m:
        return None, None
    art_roh, nummer = m.group(1).lower(), m.group(2)
    if art_roh.startswith(("anhang", "annex")):
        norm, nummer = "Anhang", nummer.upper()
        rest = _NR.search(fundstelle[m.end():])
        unter = f"Nr. {rest.group(1)}" if rest else None
    else:
        norm = "§" if art_roh.startswith(("§", "paragra")) else "Art."
        nummer = nummer.lower()
        rest = _ABS.search(fundstelle[m.end():])
        unter = f"Abs. {rest.group(1) or rest.group(2)}" if rest else None
    return f"{norm} {nummer}", unter


def fundstelle_text(fundstelle: str) -> str:
    art, unter = norm_fundstelle(fundstelle)
    if art is None:
        return " ".join((fundstelle or "").split())
    return f"{art} {unter}" if unter else art
