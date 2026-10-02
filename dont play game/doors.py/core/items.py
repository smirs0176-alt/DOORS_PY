import abc

class BaseItem(abc.ABC):
    def __init__(self, name: str, description: str, uses: int = 1):
        self.name = name
        self.description = description
        self.uses = uses  # Количество прочности/зарядов (1 = одноразовый)

    @abc.abstractmethod
    def use(self, player, room) -> bool:
        """Логика применения предмета. Возвращает True, если предмет успешно использован."""
        pass


# 1. ФОНАРИК
class Flashlight(BaseItem):
    def __init__(self):
        super().__init__(
            name="Фонарик", 
            description="Освещает тёмные комнаты. Заряда хватает на 3 использования.", 
            uses=3
        )

    def use(self, player, room) -> bool:
        if room.is_dark:
            print("\n[🔦] Вы включили фонарик! Тёмная комната стала полностью освещённой.")
            room.is_dark = False
            self.uses -= 1
            print(f"🔋 Ост. заряда фонарика: {self.uses}")
            return True
        else:
            print("\n[ℹ️] В комнате и так светло, использовать фонарик нет смысла.")
            return False


# 2. ОТМЫЧКИ
class Lockpick(BaseItem):
    def __init__(self):
        super().__init__(
            name="Отмычки", 
            description="Позволяет моментально взломать запертую дверь без поиска ключа.", 
            uses=1
        )

    def use(self, player, room) -> bool:
        if room.is_locked:
            print("\n[🗝️] Вы умело подковырнули замок отмычкой! Дверь открыта.")
            room.is_locked = False
            self.uses -= 1
            return True
        else:
            print("\n[ℹ️] Эта дверь не заперта.")
            return False


# 3. ПОДЖИГАЛОЧКА (Зажигалка)
class Lighter(BaseItem):
    def __init__(self):
        super().__init__(
            name="Поджигалочка", 
            description="Слабый источник света. Даёт 5 быстрых вспышек в темноте.", 
            uses=5
        )

    def use(self, player, room) -> bool:
        if room.is_dark:
            print("\n[🔥] Вы чиркнули поджигалочкой! Небольшой огонек разгнал тьму.")
            room.is_dark = False
            self.uses -= 1
            print(f"🔥 Ост. использования зажигалки: {self.uses}")
            return True
        else:
            print("\n[ℹ️] Здесь и так достаточно светло.")
            return False


# 4. ТАБЛЕТОЧКИ
class Pills(BaseItem):
    def __init__(self):
        super().__init__(
            name="Таблеточки", 
            description="Восстанавливают 40 HP.", 
            uses=1
        )

    def use(self, player, room) -> bool:
        if player.health < player.max_health:
            healed = min(40, player.max_health - player.health)
            player.heal(40)
            print(f"\n[💊] Вы выпили таблеточки и восстановили +{healed} HP!")
            self.uses -= 1
            return True
        else:
            print("\n[ℹ️] У вас и так полное здоровье!")
            return False