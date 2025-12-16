import random
import psycopg
import os
from datetime import datetime

ammo = 0
shots = 0
mag = []


def get_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id SERIAL PRIMARY KEY,
                    played_at TIMESTAMP NOT NULL,
                    ammo INTEGER NOT NULL,
                    death_shot INTEGER,
                    survived BOOLEAN NOT NULL
                )
            """)


def save_round(ammo: int, death_shot: int | None):
    survived = death_shot is None
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_history (played_at, ammo, death_shot, survived)
                VALUES (%s, %s, %s, %s)
            """, (datetime.now(), ammo, death_shot, survived))


def show_history(limit: int = 10):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, played_at, ammo, death_shot, survived
                FROM game_history
                ORDER BY id DESC
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()

    print(f"\n=== Ostatnie {limit} gier ===")
    if not rows:
        print("Brak zapisanych gier.\n")
        return

    for game_id, played_at, ammo, death_shot, survived in rows:
        if survived:
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
    chances = (empty_chambers / 6) * 100
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
            break
        elif choice == "r":
            restart_game()
            continue

        shots += 1
        print(f"Strzał numer {shots}")
        current_chamber = mag[shots - 1]

        if current_chamber == 1:
            print("ZGON! Trafiłeś na nabój.\n")
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
    deaths_per_shot = {i: 0 for i in range(1, 7)}
    survived = 0

    for _ in range(amount_of_games):
        result = one_game_sim(ammo)
        if result is None:
            survived += 1
        else:
            deaths_per_shot[result] += 1

    print("======= Game Simulation =======")
    for shot in range(1, 7):
        pps = (deaths_per_shot[shot] / amount_of_games) * 100
        print(f"Strzał numer {shot}: zgon na tym strzale: {pps:.0f}%")


def main_menu():
    while True:
        print("=== ROSYJSKA RULETKA ===")
        print("[g] – normalna gra")
        print("[s] – symulacja wielu gier")
        print("[h] – historia gier")
        print("[q] – wyjście")
        mode = input("Wybierz tryb: ").strip().lower()

        if mode == "g":
            normal_game()
        elif mode == "s":
            ammo = int(input("Podaj liczbę naboi (0–6): "))
            games = int(input("Podaj liczbę gier do symulacji: "))
            simulation(ammo, games)
        elif mode == "h":
            show_history(20)
        elif mode == "q":
            break


if __name__ == "__main__":
    init_db()
    main_menu()
