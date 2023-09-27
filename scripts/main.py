"""
Главный модуль приложения
Авторы: Мишенин Р.М., Некеров Я.А., БИВ222
"""
import tkinter as tk
import pandas as pd
import configparser
import os
import sys
import pathlib
from pathlib import Path

# изменение системного пути к каталогу
os.chdir(os.path.abspath(os.getcwd())[:-8])
sys.path.insert(1, os.path.abspath(os.getcwd()))
# импорт необходимых модулей
from library.generalfunc import create_guide
from specialfunc import (
    ask_param,
    ask_stat,
    graph_weight,
    graph_goods,
    ask_pivot,
    graph_dist,
    graph_load,
)

# чтение данных из ini файла и присваивание значений переменной
config = configparser.ConfigParser()
config.read(Path(pathlib.Path.cwd(), "scripts", "configuration.ini"))

colorback = config["settings"]["colorback"]
colortext = config["settings"]["colortext"]
bt_font = config["settings"]["bt_font"].split(",")
bt_font[1] = int(bt_font[1])
bt_font = tuple(bt_font)
lb_font = config["settings"]["lb_font"].split(",")
lb_font[1] = int(lb_font[1])
lb_font = tuple(lb_font)
# создание главного окна проекта
root = tk.Tk()
root.geometry("700x640+650+40")
root.focus_force()
root.title("Главное окно")
root.resizable(False, False)
root.config(bg=colorback)
ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "hello.png"))
root.iconphoto(False, ph)

lb_tables = tk.Label(root, text="Таблицы", fg=colortext, bg=colorback, font=lb_font)
lb_tables.place(x=270, y=0)
# здесь и далее - создание виджетов Button и Label для оформления меню
bt_main = tk.Button(
    root,
    text="Основная",
    fg=colorback,
    bg=colortext,
    width=19,
    height=2,
    command=lambda: create_guide(
        root,
        "Основной справочник",
        "600x250+30+30",
        str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_main.place(x=20, y=55)

bt_hold = tk.Button(
    root,
    text="Владельцы",
    fg=colorback,
    bg=colortext,
    width=18,
    height=2,
    command=lambda: create_guide(
        root,
        "Справочник владельцев",
        "500x150+30+350",
        str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_hold.place(x=365, y=55)

lb_text = tk.Label(
    root, text="Текстовые отчёты", fg=colortext, bg=colorback, font=lb_font
)
lb_text.place(x=200, y=145)

bt_prod = tk.Button(
    root,
    text="Продукты от\n владельца",
    fg=colorback,
    bg=colortext,
    width=12,
    height=2,
    command=lambda: ask_param(
        root,
        'Отчёт "продукты от владельца"',
        "500x100+30+580",
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        ),
        str(Path(pathlib.Path.cwd(), "output", "Products.csv")),
        "Введите № владельца:",
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_prod.place(x=20, y=200)

bt_tray = tk.Button(
    root,
    text="Загруженность\nстеллажа",
    fg=colorback,
    bg=colortext,
    width=12,
    height=2,
    command=lambda: ask_param(
        root,
        'Отчёт "загруженность стеллажа"',
        "350x100+156+484",
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        ),
        str(Path(pathlib.Path.cwd(), "output", "Trays.csv")),
        "Введите № стеллажа:",
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_tray.place(x=235, y=200)

bt_cure = tk.Button(
    root,
    text="Необходимость\nпоставки",
    fg=colorback,
    bg=colortext,
    width=13,
    height=2,
    command=lambda: ask_param(
        root,
        'Отчёт "необходимость поставки"',
        "400x200+195+143",
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        ),
        str(Path(pathlib.Path.cwd(), "output", "Procurement.csv")),
        "Минимальное кол-во:",
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_cure.place(x=450, y=200)

bt_stat = tk.Button(
    root,
    text="Общая статистика",
    fg=colorback,
    bg=colortext,
    width=19,
    height=2,
    font=bt_font,
    command=lambda: ask_stat(
        root,
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        ),
    ),
    relief="raised",
    bd=1,
)
bt_stat.place(x=20, y=290)

bt_pivot = tk.Button(
    root,
    text="Сводная таблица",
    fg=colorback,
    bg=colortext,
    width=18,
    height=2,
    font=bt_font,
    command=lambda: ask_pivot(
        root,
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        ),
    ),
    relief="raised",
    bd=1,
)
bt_pivot.place(x=365, y=290)

lb_graph = tk.Label(
    root, text="Графические отчёты", fg=colortext, bg=colorback, font=lb_font
)
lb_graph.place(x=185, y=380)

bt_goods = tk.Button(
    root,
    text="Товары на стеллаж",
    fg=colorback,
    bg=colortext,
    width=19,
    height=2,
    command=lambda: graph_goods(
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        )
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_goods.place(x=20, y=440)

bt_weight = tk.Button(
    root,
    text="Вес на стеллажах",
    fg=colorback,
    bg=colortext,
    width=18,
    height=2,
    command=lambda: graph_weight(
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        )
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_weight.place(x=365, y=440)

bt_dist = tk.Button(
    root,
    text="Распределение весов",
    fg=colorback,
    bg=colortext,
    width=19,
    height=2,
    command=lambda: graph_dist(
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        )
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_dist.place(x=20, y=530)

bt_load = tk.Button(
    root,
    text="Загруженность склада",
    fg=colorback,
    bg=colortext,
    width=18,
    height=2,
    command=lambda: graph_load(
        pd.merge(
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Main.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            pd.read_csv(
                str(Path(pathlib.Path.cwd(), "data", "Holders.csv")),
                delimiter=",",
                encoding="utf8",
            ),
            on="Владелец №",
        )
    ),
    font=bt_font,
    relief="raised",
    bd=1,
)
bt_load.place(x=365, y=530)

# запуск приложения
root.mainloop()
