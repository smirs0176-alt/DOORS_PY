import abc

class BaseEntity(abc.ABC):
    def __init__(self, name: str, spawn_chance: float):
        self.name = name
        self.spawn_chance = spawn_chance

    @abc.abstractmethod
    def can_spawn(self, room) -> bool:
        """Проверяет условия, может ли сущность появиться в этой комнате."""
        pass

    @abc.abstractmethod
    def trigger(self, player, room) -> bool:
        """Логика атаки сущности. Возвращает True если игрок выжил, False если умер."""
        pass