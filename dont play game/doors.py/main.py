import sys
from core.display import Display
from core.menu import MainMenu
from core.engine import GameEngine
from core.rooms_engine import RoomsEngine
from core.player import Player

def main():
    while True:
        action = MainMenu.show()

        if action == "exit":
            Display.clear_screen()
            print("До встречи в следующем заезде!")
            sys.exit()

        elif action == "start_hotel":
            engine = GameEngine()
            while engine.player.is_alive():
                survived = engine.play_turn()
                if not survived:
                    break

        elif action == "start_rooms":
            player = Player()
            rooms_engine = RoomsEngine(player)
            rooms_engine.start()

if __name__ == "__main__":
    main()