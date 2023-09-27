"""
Модуль с библиотеками, созданными специально для данного приложения
Авторы: Мишенин Р.М., Некеров Я.А., БИВ222
"""
import tkinter as tk
import pandas as pd
import tkinter.messagebox as mb
import numpy as np
import configparser
import matplotlib.pyplot as plt
import pathlib
from pathlib import Path
import os
import sys
from tkinter import ttk

# изменение системного пути к файлам
os.chdir(os.path.abspath(os.getcwd()))
sys.path.insert(1, os.path.abspath(os.getcwd()))
from library.generalfunc import export, onFrameConfigure

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


def create_report(
    root: tk.Tk,
    parent: tk.Toplevel,
    title: str,
    coord: str,
    NAME: pd.DataFrame,
    param: str,
    path: str,
):
    """_summary_

    Args:
        root (tk.Tk): корневое окно
        parent (tk.Toplevel): ссылка на предыдущее окно (чтобы удалить)
        title (str): название окна
        coord (str): размеры окна
        NAME (pd.DataFrame): DataFrame
        param (str): ключевой параметр, по которому будет строиться 1 из 3 отчетов
        path (str): путь к файлу
    """
    flag = False
    if title == 'Отчёт "продукты от владельца"':
        if (
            not param.isdigit()
            or int(param) > NAME["Владелец №"].max()
            or int(param) <= 0
        ):
            mb.showerror(
                "Неверный идентификатор владельца",
                "Введите корректный номер владельца!",
            )
            parent.focus_force()
        else:
            flag = True
            SEL = NAME["Владелец №"] == int(param)
            NAME = NAME.loc[SEL, ["Название", "Фамилия", "Имя", "Отчество"]]
    elif title == 'Отчёт "загруженность стеллажа"':
        if (
            not param.isdigit()
            or int(param) > NAME["Стеллаж №"].max()
            or int(param) <= 0
        ):
            mb.showerror(
                "Неверный номер стеллажа", "Введите корректный номер стеллажа!"
            )
            parent.focus_force()
        else:
            flag = True
            SEL = NAME["Стеллаж №"] == int(param)
            NAME = NAME.loc[SEL, ["Название", "Остаток", "Масса (кг)"]]
    else:
        if not param.isdigit() or int(param) <= 0:
            mb.showerror(
                "Неверное количество товара", "Введите корректный количество товара!"
            )
            parent.focus_force()
        else:
            flag = True
            SEL = NAME["Остаток"] <= int(param)
            NAME = NAME.loc[SEL, ["Название", "Остаток", "Владелец №"]]
    if flag:
        parent.destroy()
        win = tk.Toplevel(root)
        win.geometry(coord)
        mainmenu = tk.Menu(win)
        win.config(menu=mainmenu)
        win.focus_force()
        ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "table.png"))
        win.iconphoto(False, ph)
        win.resizable(False, True)
        win.title(title)
        # создание сложной структуры из Canvas, Frame для использования Scrollbar
        canvas = tk.Canvas(win, borderwidth=0)
        frame = tk.Frame(canvas)
        scroll = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((1, 1), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        height = NAME.shape[0]
        width = NAME.shape[1]
        mainmenu.add_command(label="Экспорт", command=lambda: export(win, NAME, path))
        pnt = np.empty(shape=(height + 1, width), dtype="O")
        vrs = np.empty(shape=(height + 1, width), dtype="O")
        # заполнение виджетов Entry значениями
        for i in range(height + 1):
            for j in range(width):
                if i == 0:
                    e = tk.Entry(frame, relief="ridge")
                    e.grid(row=0, column=j, sticky=tk.E)
                    e.insert(tk.END, NAME.columns[j])
                    e.config(state="readonly")
                else:
                    vrs[i, j] = tk.StringVar()
                    pnt[i, j] = tk.Entry(frame, textvariable=vrs[i, j])
                    pnt[i, j].grid(row=i, column=j)
                    cnt = NAME.iloc[i - 1, j]
                    vrs[i, j].set(str(cnt))
                    pnt[i, j].config(state="readonly")


def ask_param(
    root: tk.Tk, title: str, coord: str, NAME: pd.DataFrame, path: str, msg: str
):
    """_summary_

    Args:
        root (tk.Tk): корневое окно
        title (str): название окна
        coord (str): размеры окна
        NAME (pd.DataFrame): DataFrame
        path (str): путь к файлу, куда идет сохранение
        msg (str): сообщение, которое выводится пользователю
    """
    win = tk.Toplevel(root)
    win.geometry("500x150+700+200")
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "question.png"))
    win.iconphoto(False, ph)
    win.resizable(False, False)
    win.title("Окно выбора")
    win.config(bg=colorback)
    lb_msg = tk.Label(win, text=msg, fg=colortext, bg=colorback, font=lb_font)
    lb_msg.place(x=20, y=20)
    entry = tk.Entry(win, font=("Arial", 18, "bold"), width=5)
    entry.place(x=420, y=30)
    btn = tk.Button(
        win,
        text="OK",
        font=bt_font,
        bg=colortext,
        fg=colorback,
        command=lambda: create_report(root, win, title, coord, NAME, entry.get(), path),
    )
    btn.place(x=200, y=80)
    if title == 'Отчёт "продукты от владельца"':
        mb.showinfo(
            "Инструкция",
            "Введите номер владельца, чтобы получить информацию о всех его товарах",
        )
    elif title == 'Отчёт "загруженность стеллажа"':
        mb.showinfo(
            "Инструкция",
            "Введите номер стеллажа, чтобы получить информацию о товарах, расположенных на нём",
        )
    else:
        mb.showinfo(
            "Инструкция",
            "Введите минимальное количество единиц товара, чтобы узнать, что нужно заказать",
        )
    entry.focus_force()


def ask_stat(root: tk.Tk, NAME: pd.DataFrame):
    """_summary_

    Args:
        root (tk.Tk): ссылка на корневое окно
        NAME (pd.DataFrame): DatFrame
        Функция узнает у пользователя, отчёт по какому атрибуту он хотел бы увидеть
    """
    win = tk.Toplevel(root)
    win.geometry("430x120+700+200")
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "question.png"))
    win.iconphoto(False, ph)
    win.resizable(False, False)
    win.title("Окно выбора")
    win.config(bg=colorback)
    lb_msg = tk.Label(
        win, text="Выберите переменную:", fg=colortext, bg=colorback, font=lb_font
    )
    lb_msg.place(x=10, y=0)
    com_col = ttk.Combobox(
        win,
        values=[
            "Название",
            "Владелец №",
            "Остаток",
            "Стеллаж №",
            "Масса (кг)",
            "Фамилия",
            "Имя",
            "Отчество",
        ],
        font=bt_font,
        width=12,
        state="readonly",
    )
    com_col.current(0)
    com_col.place(x=30, y=60)
    com_col.focus_force()
    # намеренное переключение фокуса на окно
    btn = tk.Button(
        win,
        text="OK",
        font=bt_font,
        bg=colortext,
        fg=colorback,
        command=lambda: create_stat(root, win, NAME, com_col.get()),
    )
    btn.place(x=330, y=50)


def create_stat(root: tk.Tk, parent: tk.Toplevel, NAME: pd.DataFrame, answer: str):
    """_summary_

    Args:
        root (tk.Tk): ссылка на корневое окно
        parent (tk.Toplevel): ссылка на предыдущее окно
        NAME (pd.DataFrame): DataFrame
        answer (str): ответ пользователя, который получаем из функции ask_stat()
    """
    parent.destroy()
    win = tk.Toplevel(root)
    mainmenu = tk.Menu(win)
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "table.png"))
    win.iconphoto(False, ph)
    win.config(menu=mainmenu)
    win.focus_force()
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "table.png"))
    win.iconphoto(False, ph)
    win.resizable(True, True)
    win.title(f'"{answer}"')
    canvas = tk.Canvas(win, borderwidth=0)
    frame = tk.Frame(canvas)
    scroll = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((1, 1), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    mainmenu.add_command(
        label="Экспорт",
        command=lambda: export(
            win, NAME, Path(pathlib.Path.cwd(), "data", f"Статистика({answer}).csv")
        ),  # не уверен, что это сработает, проверь!
    )
    # проверка на тип отчёта, запрашиваемый пользователем
    if answer in ["Название", "Фамилия", "Имя", "Отчество", "Владелец №", "Стеллаж №"]:
        win.geometry("350x200+100+100")
        W = NAME[answer].value_counts().to_frame().reset_index()
        percents = []
        for i in range(W.shape[0]):
            percents.append((W[answer].loc[W.index[i]] / NAME.shape[0] * 100).round(5))
        W["Проценты (%)"] = percents
        W.rename(
            columns={"index": f"{answer}", f"{answer}": "Количество"}, inplace=True
        )
        height = W.shape[0]
        width = W.shape[1]
        pnt = np.empty(shape=(height + 1, width), dtype="O")
        vrs = np.empty(shape=(height + 1, width), dtype="O")
        for i in range(height + 1):
            for j in range(width):
                if i == 0:
                    e = tk.Entry(frame, relief="ridge")
                    e.grid(row=0, column=j, sticky=tk.E)
                    e.insert(tk.END, W.columns[j])
                    e.config(state="readonly")
                else:
                    vrs[i, j] = tk.StringVar()
                    pnt[i, j] = tk.Entry(frame, textvariable=vrs[i, j])
                    pnt[i, j].grid(row=i, column=j)
                    cnt = W.iloc[i - 1, j]
                    vrs[i, j].set(str(cnt))
                    pnt[i, j].config(state="readonly")
    else:
        win.geometry("250x140+50+50")
        NAME = NAME[answer].describe().to_frame().reset_index()
        height = 8
        width = 2
        pnt = np.empty(shape=(height, width), dtype="O")
        vrs = np.empty(shape=(height, width), dtype="O")
        lst = [
            "Количество",
            "Среднее",
            "СТД Отклонение",
            "Минимум",
            "25%",
            "50%",
            "75%",
            "Максимум",
        ]
        for i in range(height):
            e = tk.Entry(frame, relief="ridge")
            e.grid(row=i, column=0, sticky=tk.E)
            e.insert(tk.END, lst[i])
            e.config(state="readonly")
        for i in range(height):
            vrs[i, 1] = tk.StringVar()
            pnt[i, 1] = tk.Entry(frame, textvariable=vrs[i, 1])
            pnt[i, 1].grid(row=i, column=1)
            cnt = NAME.iloc[i, 1]
            vrs[i, 1].set(str(cnt.round(5)))
            pnt[i, 1].config(state="readonly")


def ask_pivot(root: tk.Tk, NAME: pd.DataFrame):
    """_summary_

    Args:
        root (tk.Tk): ссылка на корневое окно
        NAME (pd.DataFrame): DataFrame
        Функция запрашивает у пользователя параметры для формирования сводной таблицы
    """
    win = tk.Toplevel(root)
    win.geometry("600x220+700+200")
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "question.png"))
    win.iconphoto(False, ph)
    win.resizable(False, False)
    win.title("Окно выбора")
    win.config(bg=colorback)
    lb_msg = tk.Label(
        win,
        text="Выберите РАЗЛИЧНЫЕ переменные:",
        fg=colortext,
        bg=colorback,
        font=bt_font,
    )
    lb_msg.place(x=10, y=0)
    com_1 = ttk.Combobox(
        win,
        values=["Название", "Владелец №", "Стеллаж №", "Фамилия", "Имя", "Отчество"],
        font=bt_font,
        width=12,
        state="readonly",
    )
    com_1.current(0)
    com_1.place(x=30, y=50)
    com_1.focus_force()
    com_2 = ttk.Combobox(
        win,
        values=["Название", "Владелец №", "Стеллаж №", "Фамилия", "Имя", "Отчество"],
        font=bt_font,
        width=12,
        state="readonly",
    )
    com_2.current(1)
    com_2.place(x=330, y=50)
    lb_agg = tk.Label(
        win,
        text="Выберите агрегирующую функцию:",
        fg=colortext,
        bg=colorback,
        font=bt_font,
    )
    lb_agg.place(x=10, y=100)
    com_agg = ttk.Combobox(
        win,
        values=[
            "mean (Среднее)",
            "median (Медиана)",
            "min (Минимум)",
            "max (Максимум)",
            "std (СТД Отклонение)",
            "sum (Сумма)",
        ],
        font=bt_font,
        width=15,
        state="readonly",
    )
    com_agg.current(0)
    com_agg.place(x=70, y=160)
    btn = tk.Button(
        win,
        text="OK",
        font=bt_font,
        bg=colortext,
        fg=colorback,
        command=lambda: create_pivot(
            root, win, NAME, com_1.get(), com_2.get(), com_agg.get()
        ),
    )
    btn.place(x=370, y=150)


def create_pivot(
    root: tk.Tk,
    parent: tk.Toplevel,
    NAME: pd.DataFrame,
    par1: str,
    par2: str,
    aggr: str,
):
    """_summary_

    Args:
        root (tk.Tk): ссылка на корневое окно
        parent (tk.Toplevel): ссылка на окно с выбором (чтобы удалить)
        NAME (pd.DataFrame): DataFrame
        par1 (str): первый параметр (строки)
        par2 (str): второй параметр (столбцы)
        aggr (str): аггрегирующая функция
    """
    parent.destroy()
    if par1 == par2:
        # обработка ошибки:выбор двух одинаковых переменных
        mb.showerror("Ошибка выбора", "Введите РАЗЛИЧНЫЕ параметры!")
        ask_pivot(root, NAME)
    else:
        win = tk.Toplevel(root)
        win.geometry("600x300+100+100")
        ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "table.png"))
        win.iconphoto(False, ph)
        mainmenu = tk.Menu(win)
        win.config(menu=mainmenu)
        win.focus_force()
        ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "table.png"))
        win.iconphoto(False, ph)
        win.resizable(False, True)
        win.title("Сводная таблица")
        canvas = tk.Canvas(win, borderwidth=0)
        frame = tk.Frame(canvas)
        scrollv = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollv.set)
        scrollg = tk.Scrollbar(win, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollg.set)
        scrollg.pack(side="bottom", fill="x")
        scrollv.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((1, 1), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        NAME = NAME.pivot_table(
            index=par1,
            columns=par2,
            values=["Масса (кг)", "Остаток"],
            aggfunc=aggr[: aggr.find("(") - 1],
        )
        height = NAME.shape[0]
        width = NAME.shape[1]
        mainmenu.add_command(
            label="Экспорт",
            command=lambda: export(
                win, NAME, Path(pathlib.Path.cwd(), "data", "Pivot.csv")
            ),
        )
        pnt = np.empty(shape=(height + 2, width + 1), dtype="O")
        vrs = np.empty(shape=(height + 2, width + 1), dtype="O")
        for i in range(height + 1):
            e = tk.Entry(frame, relief="ridge")
            e.grid(row=i, column=0, sticky=tk.E)
            if i == 0:
                e.insert(tk.END, "Мульти-индекс")
            else:
                e.insert(tk.END, NAME.index[i - 1])
            e.config(state="readonly")
            for j in range(1, width + 1):
                if i == 0:
                    e = tk.Entry(frame, relief="ridge")
                    e.grid(row=0, column=j, sticky=tk.E)
                    e.insert(
                        tk.END,
                        str(NAME.columns[j - 1])
                        .replace("{", "")
                        .replace("}", "")
                        .replace("'", ""),
                    )
                    e.config(state="readonly")
                else:
                    vrs[i, j] = tk.StringVar()
                    pnt[i, j] = tk.Entry(frame, textvariable=vrs[i, j])
                    pnt[i, j].grid(row=i, column=j)
                    cnt = NAME.iloc[i - 1, j - 1]
                    vrs[i, j].set(str(cnt.round(1)).replace("nan", "-"))
                    pnt[i, j].config(state="readonly")


def graph_goods(NAME: pd.DataFrame):
    """_summary_

    Args:
        NAME (pd.DataFrame): DataFrame
        Создаёт графический отчёт типа стобчатая диаграмма
    """
    NAME = NAME.groupby(["Стеллаж №"]).agg({"Остаток": "sum"}).reset_index()
    trays = NAME["Стеллаж №"].to_list()
    number = NAME["Остаток"].to_list()
    fig, ax = plt.subplots()
    bar_container = ax.bar(trays, number)
    ax.set(
        ylabel="Количество",
        title="Остаток товаров на стеллажах",
        ylim=(0, max(number) + 30),
        xlabel="Стеллаж №",
    )
    ax.bar_label(bar_container)
    plt.show()


def graph_weight(NAME: pd.DataFrame):
    """_summary_

    Args:
        NAME (pd.DataFrame): DataFrame
        Создаёт графический отчёт типа диаграмма Бокса-Вискера
    """
    values = []
    for i in range(1, NAME["Стеллаж №"].max() + 1):
        values.append(mass_on_each_tray(NAME, i))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(values)
    ax.set_xlabel("Стеллаж №")
    ax.set_ylabel("Масса (кг)")
    plt.title("Загруженность стеллажей")
    plt.show()


def mass_on_each_tray(NAME: pd.DataFrame, num: int) -> list:
    """_summary_

    Args:
        NAME (pd.DataFrame): DataFrame
        num (int): номер стеллажа, для которого нужно создать список с массами всех товаров, лежащих на нём

    Returns:
        list: список с массами товаров
    """
    lst = []
    for i in range(NAME.shape[0]):
        if NAME["Стеллаж №"].loc[NAME.index[i]] == num:
            lst.append(
                NAME["Остаток"].loc[NAME.index[i]]
                * NAME["Масса (кг)"].loc[NAME.index[i]]
            )
    lst = list(np.around(np.array(lst), 1))
    return lst


def graph_dist(NAME: pd.DataFrame):
    """_summary_

    Args:
        NAME (pd.DataFrame): DataFrame
        Создаёт графический отчёт типа гистограмма
    """
    data = NAME["Масса (кг)"].to_list()
    fig, ax = plt.subplots()
    bar_container = ax.hist(data, bins=100)
    plt.hist(data, bins=50)
    ax.set(ylabel="Количество", xlabel="Масса (кг)")
    plt.title("Распределение масс")
    plt.show()


def graph_load(NAME: pd.DataFrame):
    """_summary_

    Args:
        NAME (pd.DataFrame): DataFrame
        Создаёт графический отчёт типа диаграмма рассеивания
    """
    weights = NAME["Масса (кг)"].to_list()
    lefts = NAME["Остаток"].to_list()
    res_list = [weights[i] * lefts[i] for i in range(len(weights))]
    fig, ax = plt.subplots()
    bar_container = ax.scatter(weights, lefts, s=res_list, c="orange")
    ax.set(ylabel="Остаток", xlabel="Масса (кг)")
    plt.text(18, 100, "Размер круга = [кг*шт]")
    plt.title("Загруженность склада")
    plt.show()
