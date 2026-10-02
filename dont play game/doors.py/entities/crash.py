import time
import random
from entities.base_entity import BaseEntity

class Crash(BaseEntity):
    def __init__(self):
        super().__init__(name="Краш", spawn_chance=0.20)

    def trigger(self, player, room) -> bool:
        print("\n" + "💥" * 25)
        print("💥 [УДАР!] Краш выбивает двери лестничного пролёта!")
        print("💥" * 25)

        start_time = time.time()
        action = input("СРОЧНО! Введи 'уклониться' или 'шкаф': ").strip().lower()
        elapsed = time.time() - start_time

        if action in ["уклониться", "шкаф"] and elapsed <= 1.8:
            print("🛡️ Вы вовремя отскочили от летящих обломков дверей!")
            return True
        else:
            print("💀 Краш снёс вас вместе с дверной рамой...")
            player.take_damage(100)
            return False

def setup():
    return Crash()