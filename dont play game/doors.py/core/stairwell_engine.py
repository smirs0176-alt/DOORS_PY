import random
from core.player import Player
from core.shop_badges import BadgeManager
from entities.crash import Crash
from entities.brush import Brush
from entities.bleach import Bleach

class StairwellEngine:
    def __init__(self, player: Player):
        self.player = player
        self.stair_count = 1
        self.monsters = [Crash(), Brush(), Bleach()]

    def start(self) -> bool:
        BadgeManager.unlock_badge("stairwell_runner")
        print("\n" + "🪜" * 30)
        print("🚪 ВЫ СТУПИЛИ НА БЕСКОНЕЧНУЮ ЛЕСТНИЦУ: THE STAIRWELL")
        print("⚠️ Эхо шагов разносится вниз... Внимательно следите за тьмой!")
        print("🪜" * 30)

        while self.player.is_alive():
            print(f"\n--------------------------------------------------")
            print(f"❤️ HP: {self.player.health} | 🪜 Пролёт вниз #{self.stair_count}")
            print(f"--------------------------------------------------")

            # Шанс атаки новых монстров
            if random.random() < 0.40:
                monster = random.choice(self.monsters)
                survived = monster.trigger(self.player, None)
                
                if not survived:
                    return False
                
                if monster.name == "Блич":
                    BadgeManager.unlock_badge("bleach_survivor")

            print("\nДействия:")
            print("1. Спускаться ниже")
            print("2. Инвентарь")
            choice = input("Выбор: ").strip()

            if choice == "2":
                self.player.show_inventory()

            self.stair_count += 1
            if self.stair_count >= 50:
                print("\n🎉 Вы успешно преодолели 50 пролётов The Stairwell и вернулись!")
                return True

        return False