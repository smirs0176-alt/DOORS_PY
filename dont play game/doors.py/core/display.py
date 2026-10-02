import os
import time

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_RED = "\033[41m"
    BG_BLACK = "\033[40m"

class Display:
    @staticmethod
    def clear_screen():
        """Очистка консоли для эффекта переключения окон."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_logo():
        print(f"{Colors.RED}{Colors.BOLD}")
        print(r"""
  ██████╗  ██████╗  ██████╗ ██████╗  ██████╗
  ██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗██╔════╝
  ██║  ██║██║   ██║██║   ██║██████╔╝╚█████╗  
  ██║  ██║██║   ██║██║   ██║██╔══██╗ ╚═══██╗ 
  ██████╔╝╚██████╔╝╚██████╔╝██║  ██║██████╔╝ 
  ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  
        [ TEXT EDITION & THE ROOMS ]
        """ + Colors.RESET)

    @staticmethod
    def animate_door_open(room_num: int, is_rooms: bool = False):
        """Анимация открытия двери."""
        Display.clear_screen()
        prefix = "A-" if is_rooms else ""
        color = Colors.CYAN if is_rooms else Colors.YELLOW

        frame1 = f"""
        +-----------------------+
        |       [ {prefix}{room_num:03d} ]      |
        |  +-----------------+  |
        |  |                 |  |
        |  |        (o)      |  |
        |  |                 |  |
        |  +-----------------+  |
        +-----------------------+
        """
        frame2 = f"""
        +-----------------------+
        |       [ {prefix}{room_num:03d} ]      |
        |  +-------+         |  |
        |  |       |         |  |
        |  |   (o) |         |  |
        |  |       |         |  |
        |  +-------+         |  |
        +-----------------------+
        """
        print(f"{color}{frame1}{Colors.RESET}")
        time.sleep(0.15)
        Display.clear_screen()
        print(f"{color}{frame2}{Colors.RESET}")
        time.sleep(0.15)
        Display.clear_screen()

    @staticmethod
    def show_rooms_entry_art():
        """Арт входа в The Rooms за шкафом."""
        Display.clear_screen()
        print(f"{Colors.BLUE}{Colors.BOLD}")
        print(r"""
    ____________________________________________
   /                                            \
  |   [?] ВЫ ОТОДВИНУЛИ ТЯЖЕЛЫЙ ШКАФ...          |
  |                                              |
  |         +-------------------------+          |
  |         |   [ A - 0 0 0 ]         |          |
  |         |  =====================  |          |
  |         |  |  (🔒)  ОТМЫЧКА   |  |          |
  |         |  =====================  |          |
  |         +-------------------------+          |
   \____________________________________________/
        """)
        print(f"{Colors.RESET}")

    @staticmethod
    def show_monster_a60():
        print(f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}")
        print(r"""
     / \   / \     [ A - 6 0 ]
    (  o   o  )  КРАСНЫЙ ШУМ ИЗ ГЛУБИНЫ!
     \  ---  /   СРОЧНО В ШКАФ!
      \_____/
        """)
        print(f"{Colors.RESET}")

    @staticmethod
    def show_monster_a90():
        print(f"{Colors.RED}{Colors.BOLD}")
        print(r"""
      ████████████████████████████
      █  🛑  ЗАМРИ! NOT MOVE!  🛑  █
      ████████████████████████████
        """)
        print(f"{Colors.RESET}")