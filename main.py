from databaze import Databaze
from pojistenci import Pojistenci

pojistenci = Pojistenci()
databaze_pojistovna = Databaze('databaze_pojistovna')
databaze_pojistovna.vytvor_tabulku()

volba = ""
while volba != "10":
    print("------------------------------")
    print(" Evidence pojištěných")
    print("------------------------------")
    print("Vyberte si akci:")
    print("1 - Vytvoření pojištěného")
    print("2 - Vytvoření pojištění")
    print("3 - Zobrazení detailu pojištěného včetně jeho pojištění")
    print("4 - Zobrazení detailu pojištění")
    print("5 - Zobrazení seznamu pojištěných")
    print("6 - Odstranění pojištěného včetně všech jeho pojištění")
    print("7 - Odstranění pojištění")
    print("8 - Editace pojištěného")
    print("9 - Editace pojištění pojištěného")
    print("10 - Konec")
    volba = input()
    if volba == "1":
        jmeno = input("Zadejte jméno pojištěného\n")
        prijmeni = input("Zadejte příjmení\n")
        telefonni_cislo = input("Zadejte telefonní číslo\n")
        vek = input("Zadejte věk\n")
        pojistenci.vytvor_uloz_pojistnika(jmeno, prijmeni, telefonni_cislo, vek, databaze_pojistovna)
        klavesa = input("\nData byla uložena. Pokračujte libovolnou klávesou...\n")

    elif volba == "2":
        zadane_id = int(input("Zadejte ID osoby, které chcete přidat pojištění:\n"))
        nazev = input("Zadejte název pojištění\n")
        castka = int(input("Zadejte částku\n"))
        predmet = input("Zadejte předmět pojištění\n")
        platnost_od = input("Zadejte platnost od\n")
        platnost_do = input("Zadejte platnost do\n")
        pojistenci.pridej_pojisteni_pojistnika(zadane_id, nazev, castka, predmet, platnost_od, platnost_do, databaze_pojistovna)
        klavesa = input("\nPokračujte libovolnou klávesou...\n")
        
# až všechno vypíšu, tak mi to napíše, že zadané ID neexistuje!    
    elif volba == "3":
        zadane_id = int(input("Zadejte ID osoby, kterou chcete vypsat včetně pojištění:\n"))
        print(pojistenci.hledej_pojistnika(zadane_id, databaze_pojistovna))
        print(pojistenci.vypis_pojisteni_pojistnika(zadane_id, databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "4":
        zadane_id = int(input("Zadejte ID osoby, které chcete vypsat pojištění:\n"))
        print(pojistenci.vypis_pojisteni_pojistnika(zadane_id, databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "5":
        print(pojistenci.vypis_vsech_pojistniku(databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "6":
        vymaz_id = int(input("Zadejte ID osoby:\n"))
        print(pojistenci.vymaz_pojistnika(vymaz_id, databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "7":
        vymazat_id = int(input("Zadejte ID pojištění, které chcete vymazat:\n"))
        print(pojistenci.vymaz_pojisteni_pojistnika(vymazat_id, databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "8":
        editace_id = int(input("Zadejte ID osoby:\n"))
        print(pojistenci.edituj_pojistnika(editace_id, databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "9":
        editace_id = int(input("Zadejte ID pojištění:\n"))
        print(pojistenci.edituj_pojisteni(editace_id, databaze_pojistovna))
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

    elif volba == "10":
        pass
        
    else:
        print("Zadaná volba není možná")
        klavesa = input("\nPokračujte libovolnou klávesou...\n")

else:
    print("Konec")
    # elif volba == "3":
    #     hledej_id = int(input("Zadejte ID hledané osoby:\n"))
    #     print(pojistenci.hledej_pojistnika(hledej_id, databaze_pojistovna))
    #     klavesa = input("\nPokračujte libovolnou klávesou...\n")