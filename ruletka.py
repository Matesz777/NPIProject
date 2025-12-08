import keyboard
import random

ammo = 0
shots = 0
mag = []

def restartgame():
    global ammo, shots, mag
    shots = 0
    ammo = int(input("Podaj liczbe naboi(Maksymalnie 6): "))
    if ammo > 6:
        print("Maksymalna pojemność magazynka to 6 naboi. Przypisuje maksymalna wartość.")
        ammo = 6
    if ammo < 0:
        ammo = 0

    mag = [1] * ammo + [0] * (6 - ammo)
    random.shuffle(mag)
    bullets = mag.count(0)
    chances = (bullets/6) * 100

    print(f"Naciśnij klawisz '=' aby strzelić, masz {chances:.0f}% szans na przeżycie.")
    keyboard.on_press_key("=", lambda e: game(ammo))


def game(ammo):
    global shots, mag
    if shots < ammo:
        shots += 1
        print(f"Strzał numer {shots}")
        currentChamber = mag[shots - 1]

        if currentChamber == 1:
            print(f"ZGON!")
            print("Koniec gry! Chcesz grac dalej (r)? Jeśli nie to naciśnij Esc")
            keyboard.unhook_key('=')
        else:
            print(f"CYK! Jeszcze zyjesz")
    else:
        print("Koniec gry!")
        keyboard.unhook_key('=')
def onegameSim(ammo: int):
    cylinder = [1] * ammo + [0] * (6 - ammo)
    random.shuffle(cylinder)
    
    for i, bullet in enumerate(cylinder, start=1):
        if bullet == 1:
            return i
    return None

def simulation(ammo= int, amountofgames : int = 10):
    deathsPerShots = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0}
    survived = 0
    for _ in range(amountofgames):
        result = onegameSim(ammo)
        if result == None:
            survived += 1
        else:
            deathsPerShots[result] += 1
    print("=======Game Silmulation=======")
    print("===Procent wszystkich gier, w którch śmierć nastąpiła dokładnie na tym strzale===")
    for shot in range(1, 7):
        count = deathsPerShots[shot]
        if amountofgames > 0:
            pps = (count / amountofgames) * 100
        else:
            pps = 0
        print(f"Strzał numer {shot}: zgon na tym strzale: {pps:.0f}%")

     

def NewGame(e):
    restartgame()
def NewSimulation(e):
    simulation()


if __name__ == "__main__":
    mode = input("Choose mode: Normal Game[g] or Simulation[s]: ")
    if mode == "g":
        restartgame()
    elif mode == "s":
        ammo = int(input("eneter the amount of bulltes(max 6): "))
        games = int(input("eneter the amount of games: "))
        print(f"Simulation of {games} games with {ammo} bullets")
        simulation(ammo, games)
    else:
        print("Wrong mode.")

keyboard.on_press_key("r", NewGame)
keyboard.on_press_key("s", NewSimulation)
print("Restart gry 'r', Nowa symulacji 's'. Aby wyjsc z gry nacisnij 'Esc'")
keyboard.wait("esc")
