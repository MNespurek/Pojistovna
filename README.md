# Pojistovna
Aplikace pro evidenci pojištění

základní zadání:
Aplikace obsahuje správu pojištěných (to jsou pojištěné osoby, např. "Jan Novák"):
Vytvoření pojištěného
Evidujte jméno, příjmení, věk a telefonní číslo
Zobrazení seznamu všech pojištěných
Vyhledání pojištěného podle jména a příjmení
Dané entity jsou uloženy v kolekci v paměti
Aplikace je naprogramována podle dobrých praktik
Využívejte konstruktory pro inicializaci objektů
toString() pro jejich výpis
Oddělujte kód do samostatných tříd a souborů

rozšířené zadání:
Aplikace obsahuje kompletní správu (CRUD) pojištěných (např. "Jan Novák") a jejich pojištění (např. "pojištění bytu"):
Vytvoření pojištěného
Vytvoření pojištění
Zobrazení detailu pojištěného včetně jeho pojištění
Zobrazení detailu pojištění
Zobrazení seznamu pojištěných
Odstranění pojištěného včetně všech jeho pojištění
Odstranění pojištění
Editace pojištěného
Editace pojištění pojištěného
Dané entity jsou uloženy v SQL databázi
Aplikace je naprogramována podle dobrých praktik a je plně responzivní

pokročilé zadání:
Aplikace podporuje uživatelské role (pojištěný, administrátor), navrhni a implementuj, kdo vidí a může editovat jaká data
Aplikace eviduje pojistné události pojištěných, rovněž pomocí kompletní správy (CRUD)
Aplikace podporuje rozlišení pojistníků (těch, kdo platí pojištění) a pojištěných (těch, na koho se pojištění vztahuje). Místo zavedení 2 databázových tabulek se zamysli nad řešením přes výčtový typ (enum).
Aplikace generuje statistiky ve formě reportů

