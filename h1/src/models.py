"""Pydantic-Schemas für Structured Outputs und gespeicherte Ergebnisse."""
from typing import Literal

from pydantic import BaseModel, Field

Sicherheit = Literal["sicher", "unsicher"]


class RegelwerkEintrag(BaseModel):
    regelwerk: str = Field(description="Kurzform, z. B. DSGVO")
    vollstaendiger_titel: str
    ebene: Literal["EU", "Bund", "Land", "Tarif"]
    begruendung: str
    betroffene_teilprozesse: list[str] = Field(description='Nummern der Teilprozesse, z. B. ["1", "3"]')
    quelle_url: str
    fassung_datum: str
    sicherheit: Sicherheit


class Rechtsrahmen(BaseModel):
    rechtsrahmen: list[RegelwerkEintrag]


class FundLLM(BaseModel):
    """Ein Fund, wie ihn das Modell in Stufe 2 liefert."""
    regelwerk: str = Field(description="Kurzform des Regelwerks, z. B. AI Act")
    fundstelle: str = Field(description="z. B. Art. 26 Abs. 11 oder § 165")
    typ: Literal["zuordnung", "moegliche_luecke"]
    fehlender_schritt: str | None = Field(description="nur bei moegliche_luecke, sonst null")
    hinweis: str | None = Field(description="fehlendes Detail an diesem Task, sonst null")
    begruendung: str
    quelle_url: str
    fassung_datum: str
    sicherheit: Sicherheit


class Stufe2Antwort(BaseModel):
    funde: list[FundLLM]


class Fund(FundLLM):
    """Ein Fund, wie er in funde.jsonl gespeichert wird."""
    run_id: str
    fund_id: str
    task_id: str


class Meta(BaseModel):
    run_id: str
    version: str
    konfig: Literal["A", "B"]
    lauf_nr: int
    modell: str
    reasoning_effort: str
    domains: list[str]
    start: str
    ende: str | None = None
    prompt_hash_stufe1: str | None
    prompt_hash_stufe2: str
    tokens_input: int = 0
    tokens_output: int = 0
    kosten_usd_geschaetzt: float = 0.0
    suche: str = "openai"
    werkzeugaufrufe: int = 0
    werkzeugaufrufe_nicht_gefunden: int = 0
