import time
from entities.base_entity import BaseEntity

class Brush(BaseEntity):
    def __init__(self):
        super().__init__(name="Браш", spawn_chance=0.18)

    def trigger(self, player, room) -> bool:
        print("\n🎨 [ШУМ И КРАСКА] Браш замазывает лестницу тёмной суспензией!")
        print("👁️ Видимость упала до нуля!")

        start_time = time.time()
        action = input("Слушай шуршание! Введи 'присесть' чтобы пройти под ним: ").strip().lower()
        elapsed = time.time() - start_time

        if action == "присесть" and elapsed <= 2.0:
            print("✨ Браш пролетел прямо над вашей головой!")
            return True
        else:
            print("💀 Браш размазал вас по стенке лестницы...")
            player.take_damage(80)
            return player.is_alive()

def setup():
    return Brush()