import config

class Player:
    def __init__(self):
        self.health = config.START_HEALTH
        self.max_health = config.START_HEALTH
        self.is_hiding = False
        self.inventory = []  # Список предметов

    def add_item(self, item):
        if len(self.inventory) < 4:  # Максимум 4 слота
            self.inventory.append(item)
            print(f"📦 [Лут] Вы нашли предмет: {item.name}!")
        else:
            print(f"🎒 Инвентарь полон! Нельзя взять {item.name}.")

    def show_inventory(self):
        if not self.inventory:
            print("\n🎒 Ваш инвентарь пуст.")
            return

        print("\n🎒 --- ВАШ ИНВЕНТАРЬ ---")
        for idx, item in enumerate(self.inventory, 1):
            print(f"{idx}. {item.name} (Зарядов/Использований: {item.uses}) — {item.description}")

    def use_item_by_index(self, index: int, room):
        if 0 <= index < len(self.inventory):
            item = self.inventory[index]
            used_successfully = item.use(self, room)
            
            # Если сломался/расходовался полностью — удаляем
            if used_successfully and item.uses <= 0:
                print(f"🗑️ Предмет '{item.name}' полностью израсходован и выброшен.")
                self.inventory.pop(index)
        else:
            print("\n❌ Неверный номер слота!")

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount: int):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def is_alive(self) -> bool:
        return self.health > 0