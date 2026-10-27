# Masterarbeit – LaTeX

Formatvorlage aus der früheren Fassung (Drive: `Masterarbeit/masterthesis2`): KOMA `scrartcl`, 12 pt, A4, Ränder 25/25/30/25 mm, 1,5-zeilig, XeLaTeX, nummerierte Zitate.

## Bauen
```
latexmk thesis.tex      # Ergebnis: dist/thesis.pdf
```

## Vorher einmalig
- `assets/branding/hm_logo.pdf` aus Drive `masterthesis2/assets/branding/` kopieren (liegt bewusst nicht im öffentlichen Repo)
- Schrift Times New Roman für die Titelseite installiert haben (sonst Standardschrift)

## Arbeitsweise
- Inhalt entsteht im Claude Doc „Masterarbeit – Entwurf“; nur abgesegnete Sätze werden hierher übertragen.
- Offene Stellen: `\offen{...}` (rot im PDF) – vor Abgabe muss keines mehr übrig sein.
- Quellen: nur in `literatur.bib`, zitieren mit `\cite{schluessel}`.
