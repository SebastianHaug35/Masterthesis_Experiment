# Fortschritt für die Statusseite vor jedem Bauen neu berechnen
system("python3 fortschritt.py") == 0 or warn "fortschritt.py fehlgeschlagen\n";
$pdf_mode = 5;          # XeLaTeX
$bibtex_use = 2;
$out_dir = 'dist';
