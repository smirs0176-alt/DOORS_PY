import time
import random
from entities.base_entity import BaseEntity

class Bleach(BaseEntity):
    def __init__(self):
        super().__init__(name="Блич", spawn_chance=0.15)

    def trigger(self, player, room) -> bool:
        print("\n" + "🧪" * 25)
        print("🧪 [БЛИЧ!] Самый странный монстр! Он обесцвечивает и стирает реальность!")
        print("🧪" * 25)

        # Переворачиваем правильный вариант
        options = ["1", "2", "3"]
        safe_option = random.choice(options)

        print(f"🌀 Блич спутал мысли! Жми кнопку [{safe_option}]!")
        start_time = time.time()
        ans = input("Ваш выбор: ").strip()
        elapsed = time.time() - start_time

        if ans == safe_option and elapsed <= 1.5:
            print("🧪 Вы удержали разум и очистили эффект Блича!")
            return True
        else:
            print("💀 Блич полностью стёр ваше сознание...")
            player.take_damage(100)
            return False

def setup():
    return Bleach()