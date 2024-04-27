import os
import sys

"""
touhou is the best japanese game and is not an anime.
"""

class DrawConsoleTitle():
    def draw_begin_line(self) -> None:
        print("[", end='')
        print("="*60, end='')
        print("]")

    def draw_empty_line(self, total : int = 1) -> None:
        while total:
            print("[", end='')
            print(" "*60, end='')
            print("]")
            total -= 1
            
    def draw_text(self, txt, pos : int = 20) -> None:
        print("[", end='')
        print(" "*pos, end='')
        print(txt, end='')
        print(" " * int(60 - pos - len(txt)), end='')
        print("]")

    def draw(self) -> None:
        self.draw_begin_line()
        self.draw_empty_line(3)
        self.draw_text("Cartman Submit Tool")
        self.draw_empty_line(3)
        self.draw_text("By Paranormal Activity", 37)
        self.draw_begin_line()
        
    def cls(self) -> None:
        os.system("cls")
        
    def pause(self) -> None:
        os.system("pause")