from core.rooms_engine import RoomsEngine

class FloorManager:
    @staticmethod
    def enter_the_rooms(player) -> bool:
        print("\n" + "🌀" * 30)
        print("🕵️ ВЫ СЕКРЕТНО СПУСТИЛИСЬ В СЕКЦИЮ A-000 (THE ROOMS)!")
        print("🌀" * 30)
        
        # Запускаем движок The Rooms
        rooms_game = RoomsEngine(player)
        return rooms_game.start()