import time
import random
from entities.base_entity import BaseEntity

class Race(BaseEntity):
    def __init__(self):
        # Маленький шанс появления (8%), так как это неожиданный скример в шкафу
        super().__init__(name="Race", spawn_chance=0.08)

    def can_spawn(self, room) -> bool:
        # Появляется только в комнатах, где есть шкаф, начиная с 3-й комнаты
        if room.has_closet and room.number >= 3:
            return random.random() < self.spawn_chance
        return False

    def trigger(self, player, room) -> bool:
        print("\n" + "=" * 50)
        print("🚪 Вы распахиваете дверцу шкафа, чтобы спрятаться...")
        time.sleep(0.2)
        
        # Визуально-звуковой скример Рейса
        print("👁️ [СКРИМЕР] Из темноты шкафа выпрыгивает РЕЙС с жутким визгом!")
        print("😱 Рейс блокирует шкаф и выталкивает вас обратно!")
        print("=" * 50)

        # Задержка 0.5 секунды, пока Рейс улетает/исчезает
        time.sleep(0.5)

        print("\n✨ Рейс растворился в воздухе! Шкаф снова свободен, но вы потеряли время...")
        
        # Смертельность 0% — урон не наносится
        player.is_hiding = False
        return True

def setup():
    return Race()