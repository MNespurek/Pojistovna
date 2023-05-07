import sqlite3
from pojistenci import Pojistenci


pojistenci = Pojistenci()

volba = ""
while volba != "4":
    print("------------------------------")
    print(" Evidence pojištěných")
    print("------------------------------")
    print("Vyberte si akci:")
    print("1 - Přidat nového pojištěného")
    print("2 - Vypsat všechny pojištěné")
    print("3 - Vyhledat pojištěného")
    print("4 - Konec")
    print("5 - Vymaž pojistěného")
    print("6 - Edituj pojištěného")
    print("7 - Přidej pojištění")
    print("8 - Vypiš seznam pojištění pojištěného")
    volba = input()
    if volba == "1":
        jmeno = input("Zadejte jméno pojištěného\n")
        prijmeni = input("Zadejte příjmení\n")
        telefonni_cislo = input("Zadejte telefonní číslo\n")
        vek = input("Zadejte věk\n")
        pojistenci.pridej_pojistnika(jmeno, prijmeni, telefonni_cislo, vek)
        klavesa = input("\nData byla uložena. Pokračujte libovolnou klávesou...\n")
    elif volba == "2":
        print(pojistenci.vypis_pojistnika())
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
    elif volba == "3":
        jmeno = input("Zadejte jméno osoby:\n")
        prijmeni = input("Zadejte přijmení:\n")
        print(pojistenci.hledej_pojistnika(jmeno, prijmeni))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
    elif volba == "4":
        pass
    elif volba == "5":
        vymaz_id = int(input("Zadejte ID osoby:\n"))
        print(pojistenci.vymaz_pojistnika(vymaz_id))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
    elif volba == "6":
        editace_id = int(input("Zadejte ID osoby:\n"))
        print(pojistenci.edituj_pojistnika(editace_id))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
    elif volba == "7":
        zadane_id = int(input("Zadejte ID osoby, které chcete přidat pojištění:\n"))
        nazev = input("Zadejte název pojištění\n")
        castka = int(input("Zadejte částku\n"))
        predmet = input("Zadejte předmět pojištění\n")
        platnost_od = input("Zadejte platnost od\n")
        platnost_do = input("Zadejte platnost do\n")
        print(pojistenci.pridej_pojisteni_pojistnika(zadane_id, nazev, castka, predmet, platnost_od, platnost_do))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
    
    elif volba == "8":
        zadane_id = int(input("Zadejte ID osoby, které chcete vypsat pojištění:\n"))
        print(pojistenci.vypis_pojisteni_pojistnika(zadane_id))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
    else:
        print("Zadaná volba není možná")
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
else:
    print("Konec")