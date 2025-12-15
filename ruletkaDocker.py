import random
import sqlite3
from datetime import datetime

ammo = 0      
shots = 0     
mag = []

DB_PATH = "/data/ruletka.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            played_at TEXT NOT NULL,
            ammo INTEGER NOT NULL,
            death_shot INTEGER,
            survived INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_round(ammo: int, death_shot: int | None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    survived = 1 if death_shot is None else 0

    cur.execute("""
        INSERT INTO game_history (played_at, ammo, death_shot, survived)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(timespec="seconds"), ammo, death_shot, survived))

    conn.commit()
    conn.close()

def show_history(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, played_at, ammo, death_shot, survived
        FROM game_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    print(f"\n=== Ostatnie {limit} gier ===")
    if not rows:
        print("Brak zapisanych gier.\n")
        return

    for game_id, played_at, ammo, death_shot, survived in rows:
        if survived == 1:
            result_txt = "PRZEŻYŁ"
        else:
            result_txt = f"ZGON na strzale {death_shot}"
        print(f"#{game_id} | {played_at} | ammo={ammo} | {result_txt}")
    print()



def restart_game():
    global ammo, shots, mag
    shots = 0

    while True:
        try:
            ammo = int(input("Podaj liczbę naboi (0–6): "))
        except ValueError:
            print("Podaj liczbę całkowitą.")
            continue

        if ammo < 0:
            ammo = 0
        if ammo > 6:
            print("Maksymalna pojemność bębna to 6 naboi. Przypisuję 6.")
            ammo = 6

        break

    mag = [1] * ammo + [0] * (6 - ammo)
    random.shuffle(mag)

    empty_chambers = mag.count(0)
    if len(mag) > 0:
        chances = (empty_chambers / len(mag)) * 100
    else:
        chances = 100.0

    print(f"\nNowa gra! Naboje: {ammo}, puste komory: {empty_chambers}")
    print(f"Szansa przeżycia pierwszego strzału: {chances:.0f}%")


def normal_game():
    global shots, mag, ammo

    restart_game()

    while True:
        print("=== NORMALNA GRA ===")
        print("[Enter] – strzał")
        print("[r]     – nowy bęben")
        print("[q]     – powrót do menu głównego")
        choice = input("Wybierz akcję: ").strip().lower()

        if choice == "q":
            print("Powrót do menu.")
            break
        elif choice == "r":
            restart_game()
            continue
        else:
            if shots >= 6:
                print("Bęben się skończył. Losuję nowy.")
                restart_game()
                continue
            
            shots += 1
            print(f"Strzał numer {shots}")
            current_chamber = mag[shots - 1]

            if current_chamber == 1:
                print("ZGON! Trafiłeś na nabój.")
                print("Ta runda się skończyła. Wciśnij 'r' żeby losować nowy bęben, albo 'q' żeby wrócić do menu.\n")
                save_round(ammo, shots)
            else:
                print("CYK! Jeszcze żyjesz.\n")


def one_game_sim(ammo: int):
    cylinder = [1] * ammo + [0] * (6 - ammo)
    random.shuffle(cylinder)

    for i, bullet in enumerate(cylinder, start=1):
        if bullet == 1:
            return i
    return None


def simulation(ammo: int, amount_of_games: int = 10):
    deaths_per_shot = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    survived = 0

    for _ in range(amount_of_games):
        result = one_game_sim(ammo)
        if result is None:
            survived += 1
        else:
            deaths_per_shot[result] += 1

    print("======= Game Simulation =======")
    print(f"Liczba gier: {amount_of_games}, liczba naboi: {ammo}")
    print("Procent wszystkich gier, w których śmierć nastąpiła dokładnie na danym strzale:\n")

    for shot in range(1, 7):
        count = deaths_per_shot[shot]
        if amount_of_games > 0:
            pps = (count / amount_of_games) * 100
        else:
            pps = 0
        print(f"Strzał numer {shot}: zgon na tym strzale: {pps:.0f}%")

    if amount_of_games > 0:
        survive_percent = (survived / amount_of_games) * 100
        print(f"\nPrzeżycie całej gry (brak naboju): {survived} razy ({survive_percent:.0f}%)\n")


def main_menu():
    while True:
        print("=== ROSYJSKA RULETKA ===")
        print("[g] – normalna gra")
        print("[s] – symulacja wielu gier")
        print("[q] – wyjście")
        print("[h] – historia gier")
        mode = input("Wybierz tryb: ").strip().lower()

        if mode == "g":
            normal_game()
        elif mode == "s":
            try:
                ammo = int(input("Podaj liczbę naboi (0–6): "))
                games = int(input("Podaj liczbę gier do symulacji: "))
            except ValueError:
                print("Podaj poprawne liczby całkowite.")
                continue

            print(f"\nSymulacja {games} gier z {ammo} nabojami...")
            simulation(ammo, games)
        elif mode == "q":
            print("Koniec programu.")
            break
        elif mode == "h":
            show_history(20)
        else:
            print("Nieznany tryb.")


if __name__ == "__main__":
    init_db()
    main_menu()
