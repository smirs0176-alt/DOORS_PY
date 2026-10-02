import time
import random
from entities.base_entity import BaseEntity

class Drush(BaseEntity):
    def __init__(self):
        # Драш — быстрая альтернатива Рашу с шансом появления 15%
        super().__init__(name="Drush", spawn_chance=0.15)

    def can_spawn(self, room) -> bool:
        # Начинает появляться с 6-й комнаты
        if room.number >= 6:
            return random.random() < self.spawn_chance
        return False

    def trigger(self, player, room) -> bool:
        print("\n" + "=" * 50)
        print("⚡ [ВНИМАНИЕ] Свет начал дико мигать и биться об стены!")
        print("☣️ Из вентиляции вырывается плотный зелёный пар!")
        print("🔊 СЛЫШЕН БЕШЕНЫЙ СВИСТ И ГУЛ — ДРАШ ЛЕТИТ НА ОГРОМНОЙ СКОРОСТИ!")
        print("=" * 50)

        # Проверка наличия шкафа в комнате
        if not room.has_closet:
            print("\n❌ В этой комнате НЕТ ШКАФА! Вы беспомощны перед Драшем...")
            time.sleep(1.5)
            print("💀 Драш разнёс вас в дребезги на бешеной скорости!")
            player.take_damage(100)
            return False

        # Замеряем скорость реакции (у игрока есть всего 1.7 секунды)
        start_time = time.time()
        action = input("\n👉 Нажми '1' и Enter, чтобы МГНОВЕННО запрыгнуть в шкаф: ").strip()
        reaction_time = time.time() - start_time

        if action == "1" and reaction_time <= 1.7:
            print(f"\n[✓] УСПЕХ! Вы заскочили в шкаф за {round(reaction_time, 2)} сек!")
            print("💨 Драш на безумной скорости пронёсся мимо, сорвав петли со дверей...")
            player.is_hiding = True
        else:
            if reaction_time > 1.7:
                print(f"\n[❌] МЕДЛЕННО! Ваша реакция была {round(reaction_time, 2)} сек (нужно < 1.7 сек).")
            else:
                print("\n[❌] Вы замешкались и не успели войти в шкаф!")
            
            print("💀 Драш врезался в вас на полной скорости!")
            player.take_damage(100)
            return False

        # --- УНИКАЛЬНАЯ МЕХАНИКА: ЗАГАЗОВАННОСТЬ ---
        print("\n☣️ ПОСЛЕ ПРОЛЁТА ДРАША КОМНАТА ИЗНУТРИ НАПОЛНИЛАСЬ ЯДОВИТЫМ ГАЗОМ!")
        room.is_gassed = True  # Включаем флаг газа для движка engine.py

        return True

def setup():
    return Drush()