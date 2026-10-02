import random
import config
from core.items import Flashlight, Lockpick, Lighter, Pills

class Room:
    def __init__(self, number: int):
        self.number = number
        
        self.is_dark = random.random() < config.DARK_ROOM_CHANCE
        self.has_closet = random.random() < config.CLOSET_CHANCE
        self.is_locked = random.random() < 0.15  # 15% шанс запертой двери
        self.is_gassed = False
        
        # Шанс спавна лута в ящиках (35%)
        self.loot_item = self._generate_loot()

    def _generate_loot(self):
        if random.random() < 0.35:
            items_pool = [Flashlight(), Lockpick(), Lighter(), Pills()]
            return random.choice(items_pool)
        return None

    def get_description(self) -> str:
        status = []
        status.append("⚠️️ ТЕМНОТА" if self.is_dark else "💡 Светло")
        status.append("🚪 Есть шкаф" if self.has_closet else "❌ Нет шкафа")
        
        if self.is_locked:
            status.append("🔒 ДВЕРЬ ЗАПЕРТА!")
        if self.loot_item:
            status.append("📦 На столе что-то лежит")

        return f"Комната #{self.number} | " + ", ".join(status)