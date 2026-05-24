"""
Завдання 2 — фрактал "дерево Піфагора" через turtle.

Класична схема: у кожному вузлі дерева малюємо стовбур, потім
розгалуження вліво на 45° і вправо на 45°, рекурсивно. Довжина
кожної наступної гілки множиться на cos(45°) = √2/2.

Колір гілки залежить від глибини: коричневий стовбур поступово
переходить у зелений на кінчиках. Дрібниця, але дає реалістичніший
вигляд.

Управління у вікні:
  scroll — зум, ЛКМ + перетягування — пан, q — вихід.
"""

import math
import turtle


# колір від кореня (індекс 0) до листя (індекс max)
TRUNK_RGB = (0x4e, 0x34, 0x2e)   # темно-коричневий
LEAF_RGB = (0x66, 0xbb, 0x6a)    # зелений


def lerp_color(t: float) -> str:
    """Інтерполяція між коричневим (t=0) і зеленим (t=1)."""
    r = round(TRUNK_RGB[0] + (LEAF_RGB[0] - TRUNK_RGB[0]) * t)
    g = round(TRUNK_RGB[1] + (LEAF_RGB[1] - TRUNK_RGB[1]) * t)
    b = round(TRUNK_RGB[2] + (LEAF_RGB[2] - TRUNK_RGB[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def ask_level() -> int:
    while True:
        raw = input("Рівень рекурсії (рекомендовано 6-10): ").strip()
        try:
            level = int(raw)
        except ValueError:
            print("  треба число")
            continue
        if level < 0:
            print("  від'ємний рівень не має сенсу")
            continue
        if level > 12:
            confirm = input(
                f"  рівень {level} = ~{2 ** level} гілок. Точно? (y/N): "
            ).strip().lower()
            if confirm != "y":
                continue
        return level


def pythagoras(t: turtle.Turtle, length: float, level: int, max_level: int) -> None:
    """
    Рекурсивний крок: малюємо гілку довжиною length, потім
    розгалужуємо. Після обох гілок — повертаємось у вихідну точку
    і дивимось у вихідному напрямі (важливо для коректного "розкриття").
    """
    if level == 0 or length < 1:
        return

    # колір залежить від того наскільки глибоко ми зараз
    depth_ratio = (max_level - level) / max(max_level - 1, 1)
    t.pencolor(lerp_color(depth_ratio))
    t.pensize(max(1, level / 2))

    # стовбур поточної гілки
    t.forward(length)

    new_len = length * math.cos(math.radians(45))

    # ліве розгалуження
    t.left(45)
    pythagoras(t, new_len, level - 1, max_level)
    t.right(45)

    # праве розгалуження
    t.right(45)
    pythagoras(t, new_len, level - 1, max_level)
    t.left(45)

    # повертаємось назад по стовбуру
    t.backward(length)


def setup_interactions(screen) -> None:
    """Скрол = зум, ЛКМ-drag = пан, q = вихід."""
    canvas = screen.getcanvas()

    def zoom(factor: float, x: int, y: int) -> None:
        cx = canvas.canvasx(x)
        cy = canvas.canvasy(y)
        canvas.scale("all", cx, cy, factor, factor)

    canvas.bind("<MouseWheel>", lambda e: zoom(1.1 if e.delta > 0 else 1 / 1.1, e.x, e.y))
    canvas.bind("<Button-4>", lambda e: zoom(1.1, e.x, e.y))
    canvas.bind("<Button-5>", lambda e: zoom(1 / 1.1, e.x, e.y))
    canvas.bind("<ButtonPress-1>", lambda e: canvas.scan_mark(e.x, e.y))
    canvas.bind("<B1-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))
    canvas.bind_all("<KeyPress-q>", lambda _: canvas.winfo_toplevel().destroy())
    canvas.focus_set()


def draw_tree(level: int, trunk_length: float = 100) -> None:
    screen = turtle.Screen()
    screen.title(f"Дерево Піфагора — рівень {level}  (scroll = zoom, drag = pan, q = вихід)")
    screen.bgcolor("#f5f5dc")  # пісочний фон
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.left(90)  # дивимось вгору
    t.penup()
    t.goto(0, -trunk_length * 3)
    t.pendown()

    pythagoras(t, trunk_length, level, level)

    screen.update()
    setup_interactions(screen)

    print("малювання завершено. Scroll = зум, ЛКМ + drag = пан, q = вихід.")
    turtle.mainloop()


if __name__ == "__main__":
    print("Дерево Піфагора")
    print("-" * 30)
    level = ask_level()
    draw_tree(level)
