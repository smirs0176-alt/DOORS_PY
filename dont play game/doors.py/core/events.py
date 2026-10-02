import time
import random

class EventManager:
    
    # 1. ПОБЕГ ОТ СИКА (комнаты 35-40 и 70-80)
    @staticmethod
    def run_seek_chase(player, room_number: int, total_chase_rooms: int) -> bool:
        print("\n" + "🔥" * 25)
        print(f"👁️ СИК ВЫЛЕЗАЕТ ИЗ ЧЁРНОЙ ЛУЖИ! ПОБЕГ! (Комната {room_number})")
        print("🔥" * 25)

        for step in range(1, total_chase_rooms + 1):
            if not player.is_alive():
                return False

            print(f"\n🏃 Вы бежите! [Этап {step}/{total_chase_rooms}]")
            obstacle = random.choice(["дверь_налево", "дверь_направо", "Упавший_шкаф"])
            
            if obstacle == "дверь_налево":
                correct_input = "л"
                prompt = "👈 Развилка! Жми 'л' (налево): "
            elif obstacle == "дверь_направо":
                correct_input = "п"
                prompt = "👉 Развилка! Жми 'п' (направо): "
            else:
                correct_input = "пробел"
                prompt = "⚠️ УПАВШИЙ ШКАФ! Жми 'пробел' чтобы перепрыгнуть: "

            start_time = time.time()
            user_choice = input(prompt).strip().lower()
            reaction = time.time() - start_time

            # На реакцию даётся 1.6 секунды
            if user_choice == correct_input and reaction <= 1.6:
                print(f"[✓] Успешно преодолели препятствие за {round(reaction, 2)} сек!")
            else:
                print(f"\n❌ ОШИБКА ИЛИ МЕДЛЕННО ({round(reaction, 2)} сек)!")
                print("💀 Сик настиг вас и поглотил в тьму...")
                player.take_damage(100)
                return False

        print("\n🎉 Вы захлопнули тяжёлую дверь прямо перед носом Сика! Вы спаслись!")
        return True

    # 2. БИБЛИОТЕКА С НУБИНИ (Комната 50)
    @staticmethod
    def run_nubini_library(player) -> bool:
        print("\n" + "=" * 50)
        print("📚 КОМНАТА 50: БИБЛИОТЕКА НУБИНИ")
        print("🦻 Нубинька — абсолютно слепой, но слышит каждый ваш шаг!")
        print("🎯 Вам нужно собрать 3 книги и не шуметь.")
        print("=" * 50)

        books_collected = 0
        while books_collected < 3 and player.is_alive():
            print(f"\nСобрано книг: {books_collected}/3")
            action = input("Что делать? (1 - Затаить дыхание и ползти, 2 - Быстро побежать за книгой): ").strip()

            if action == "1":
                print("[🤫] Вы тихо подкрались к полке и забрали книгу!")
                books_collected += 1
            elif action == "2":
                print("\n🔊 ТУК-ТУК! Вы издали громкий звук!")
                print("👂 Нубинька услышал вас и повернул свою голову...")
                
                # Шанс спастись, если вовремя замереть
                save_action = input("СРОЧНО! Введи 'замри', чтобы Нубинька прошел мимо: ").strip().lower()
                if save_action == "замри":
                    print("[😮‍💨] Нубинька понюхал воздух и ушел дальше. Пронесло!")
                    books_collected += 1
                else:
                    print("💀 Нубинька подбежал и снёс вас!")
                    player.take_damage(100)
                    return False
            else:
                print("❌ Вы запутались и зашумели!")
                player.take_damage(50)

        print("\n🗝️ Вы нашли код, открыли замок Библиотеки и сбежали от Нубиньки!")
        return True

    # 3. МИНИ-ИГРА НА 100-Й КОМНАТЕ (Финал)
    @staticmethod
    def run_final_room_100(player) -> bool:
        print("\n" + "⚡" * 25)
        print("🚪 ФИНАЛ: КОМНАТА 100 — ЭЛЕКТРОЩИТОВАЯ")
        print("🔧 Чтобы запустить лифт, нужно починить 3 предохранителя!")
        print("⚡" * 25)

        for stage in range(1, 4):
            if not player.is_alive():
                return False

            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            correct_ans = num1 + num2

            print(f"\n⚙️ Предохранитель #{stage}: Решите замыкание! Сколько будет {num1} + {num2}?")
            start_time = time.time()
            ans = input("Ваш ответ: ").strip()
            elapsed = time.time() - start_time

            if ans == str(correct_ans) and elapsed <= 3.0:
                print(f"[⚡] Предохранитель #{stage} запущен за {round(elapsed, 1)} сек!")
            else:
                print("💥 ТОК ПОШЁЛ НЕ ТУДА! Вас ударило разрядом!")
                player.take_damage(45)

        if player.is_alive():
            print("\n🚨 ЛИФТ ЗАРАБОТАЛ! ДВЕРИ ЗАКРЫВАЮТСЯ!")
            print("🏆 ВЫ УСПЕШНО ПРОШЛИ ВСЕ 100 КОМНАТ DOORS!")
            return True
        return False