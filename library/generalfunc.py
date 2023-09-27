"""
Модуль с библиотеками, которые можно будет использовать в других проектах
Авторы: Мишенин Р.М., Некеров Я.А., БИВ222
"""
import tkinter as tk
import pandas as pd
from tkinter import ttk
import numpy as np
import configparser
import os
import tkinter.messagebox as mb
import pathlib
from pathlib import Path

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


def export(root: tk.Tk, NAME: pd.DataFrame, path: str):
    """_summary_

    Args:
        root (tk.Tk): корневой элемент
        NAME (pd.DataFrame): DataFrame
        path (str): путь к исходному файлу, откуда взяли DataFrame
        Функция собирает параметры экспорта, а по нажатию кнопки совершает его
    """
    win = tk.Toplevel(root)
    win.geometry("330x270+700+250")
    win.title("Окно экспорта")
    win.focus_force()
    win.resizable(False, False)
    win.config(bg=colorback)
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "arrow.png"))
    win.iconphoto(False, ph)
    lb_sep = tk.Label(
        win, text="Разделитель:", fg=colortext, bg=colorback, font=bt_font
    )
    lb_sep.place(x=20, y=20)
    ent_sep = tk.Entry(win, font=bt_font, width=5)
    ent_sep.place(x=220, y=20)

    lb_dec = tk.Label(
        win, text="Десятичный\n разделитель:", fg=colortext, bg=colorback, font=bt_font
    )
    lb_dec.place(x=10, y=70)
    lb_form = tk.Label(win, text="Формат:", fg=colortext, bg=colorback, font=bt_font)
    lb_form.place(x=20, y=140)
    com_form = ttk.Combobox(
        win, values=["Excel", "CSV", "Pickle"], font=bt_font, width=12, state="readonly"
    )
    com_form.current(0)
    com_form.place(x=140, y=140)
    com_dec = ttk.Combobox(
        win, values=["Запятая", "Точка"], font=bt_font, width=8, state="readonly"
    )
    com_dec.current(0)
    com_dec.place(x=190, y=80)
    bt_OK = tk.Button(
        win,
        text="OK",
        fg=colorback,
        bg=colortext,
        command=lambda: appr_exp(
            ent_sep.get(), com_form.get(), com_dec.get(), NAME, str(path)
        ),
        font=lb_font,
        relief="raised",
    )
    # при нажатии на кнопку вызывается функция appr_exp()
    bt_OK.place(x=140, y=190)


def appr_exp(sep: str, form: str, dec: str, NAME: pd.DataFrame, path: str):
    """_summary_

    Args:
        sep (str): разделитель между значениям
        form (str): формат (csv, xlsx, pick)
        dec (str): десятичный разделитель
        NAME (pd.DataFrame): DataFrame
        path (str): путь к исходному файлу, откуда взяли DataFrame
        Функция выгружает DataFrame в файловую систему
    """
    # выбор формата экспорта
    if form == "Excel":
        NAME.to_excel(
            str(path).replace("data", "output").replace("csv", "xlsx"), index=True
        )
        # показ информационного окна
        mb.showinfo(
            "Успешное сохранение",
            "Выходной файл (excel) успешно сохранён в каталоге output",
        )
    elif form == "CSV":
        # обработка ввода в поле
        if len(sep) != 1:
            mb.showerror("Ошибка ввода", 'Введите в поле "разделитель" один символ!')
        else:
            if dec == "Запятая":
                NAME.to_csv(
                    str(path).replace("data", "output"),
                    index=False,
                    decimal=",",
                    sep=sep,
                )
                mb.showinfo(
                    "Успешное сохранение",
                    "Выходной файл (csv) успешно сохранён в каталоге output",
                )
            else:
                NAME.to_csv(
                    str(path).replace("data", "output"),
                    index=False,
                    decimal=".",
                    sep=sep,
                )
                mb.showinfo(
                    "Успешное сохранение",
                    "Выходной файл (csv) успешно сохранён в каталоге output",
                )
    else:
        NAME.to_pickle(str(path).replace("data", "output").replace("csv", "pick"))
        mb.showinfo(
            "Успешное сохранение",
            "Выходной файл (pickle) успешно сохранён в каталоге output",
        )


def create_guide(root: tk.Tk, title: str, coord: str, path: str):
    """_summary_

    Args:
        root (tk.Tk): корневое окно
        title (str): название окна
        coord (str): размеры окна
        path (str): путь к исходному файлу
        Функция создает окно для показа справочников
    """
    win = tk.Toplevel(root)
    win.geometry(coord)
    mainmenu = tk.Menu(win)
    win.config(menu=mainmenu)
    win.focus_force()
    ph = tk.PhotoImage(file=Path(pathlib.Path.cwd(), "images", "table.png"))
    win.iconphoto(False, ph)
    win.resizable(False, True)
    win.title(title)
    canvas = tk.Canvas(win, borderwidth=0)
    # создание сложной структуры из Canvas, Frame для использования Scrollbar
    frame = tk.Frame(canvas)
    scroll = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((1, 1), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    NAME = pd.read_csv(str(path), delimiter=",", encoding="utf8")
    # измерение справочника в высоту и ширину
    height = NAME.shape[0]
    width = NAME.shape[1]
    mainmenu.add_command(label="Экспорт", command=lambda: export(win, NAME, path))
    actionmenu = tk.Menu(mainmenu, tearoff=0)
    mainmenu.add_cascade(label="Изменить", menu=actionmenu)
    actionmenu.add_command(
        label="Редактирование",
        command=lambda: edit_data(frame, NAME, pnt, win, root, path, title, coord),
    )
    actionmenu.add_command(
        label="Удаление",
        command=lambda: delete_data(frame, NAME, pnt, win, root, path, title, coord),
    )
    actionmenu.add_command(
        label="Добавление",
        command=lambda: add_data(frame, NAME, vrs, pnt, win, root, path, title, coord),
    )
    pnt = np.empty(shape=(height + 50, width), dtype="O")
    vrs = np.empty(shape=(height + 50, width), dtype="O")
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


def onFrameConfigure(canvas: tk.Canvas):
    """_summary_

    Args:
        canvas (tk.Canvas): для обработки скроллбара
    """
    canvas.configure(scrollregion=canvas.bbox("all"))


def delete_data(
    frame: tk.Frame,
    NAME: pd.DataFrame,
    pnt: np.array,
    parent: tk.Toplevel,
    root: tk.Tk,
    path: str,
    title: str,
    coord: str,
):
    """_summary_

    Args:
        frame (tk.Frame): фрейм, где находятся виджеты entry
        NAME (pd.DataFrame): DataFrame
        pnt (np.array): массив указателей на виджеты Entry
        parent (tk.Toplevel): предыдущее окно (чтобы удалить его)
        root (tk.Tk): корневое окно
        path (str): путь к исходому файлу
        title (str): название окна
        coord (str): размеры окна
    """
    mb.showinfo(
        "Инструкция",
        "Сотрите все значения в строке, которую хотите удалить, затем нажмите ОК (под последней строкой)",
    )
    parent.focus_force()
    # здесь и далее focus_force для фокусировки на определённом окне
    height = NAME.shape[0]
    width = NAME.shape[1]
    for i in range(1, height):
        for j in range(width):
            pnt[i, j].config(state="normal")
    btn = tk.Button(
        frame,
        text="OK",
        font=bt_font,
        bg=colortext,
        fg=colorback,
        command=lambda: appr_delete(btn, NAME, pnt, parent, root, path, title, coord),
        width=10,
    )
    btn.grid(row=height + 1, columnspan=6)


def appr_delete(
    btn: tk.Button,
    NAME: pd.DataFrame,
    pnt: np.array,
    parent: tk.Toplevel,
    root: tk.Tk,
    path: str,
    title: str,
    coord: str,
):
    """_summary_

    Args:
        btn (tk.Button): ссылка на кнопку (чтобы удалить)
        NAME (pd.DataFrame): DataFrame
        pnt (np.array): массив указателей на виджеты Entry
        parent (tk.Toplevel): предыдущее окно (чтобы удалить его)
        root (tk.Tk): корневое окно
        path (str): путь к исходому файлу
        title (str): название окна
        coord (str): размеры окна
    """
    btn.destroy()
    height = NAME.shape[0]
    width = NAME.shape[1]
    for i in range(1, height):
        lst = []
        for j in range(width):
            pnt[i, j].config(state="readonly")
            lst.append(pnt[i, j].get())
            # поиск пустой строки
            if lst == ["", "", "", "", ""]:
                for k in range(i, height - 1):
                    # цикл для удаления (переприсваивание)
                    NAME.loc[k] = NAME.iloc[k + 1]
    NAME.drop(NAME.tail(1).index, inplace=True)
    NAME.to_csv(str(path), index=False, decimal=",", sep=",")
    mb.showinfo("Успешные изменения", "Изменения успешно сохранены")
    parent.destroy()
    create_guide(root, title, coord, path)


def edit_data(
    frame: tk.Frame,
    NAME: pd.DataFrame,
    pnt: np.array,
    parent: tk.Toplevel,
    root: tk.Tk,
    path: str,
    title: str,
    coord: str,
):
    """_summary_

    Args:
        frame (tk.Frame): фрейм, где находятся виджеты entry
        NAME (pd.DataFrame): DataFrame
        pnt (np.array): массив указателей на виджеты Entry
        parent (tk.Toplevel): предыдущее окно (чтобы удалить его)
        root (tk.Tk): корневое окно
        path (str): путь к исходому файлу
        title (str): название окна
        coord (str): размеры окна
    """
    mb.showinfo(
        "Инструкция",
        "Отредактируйте необходимые записи и нажмите ОК (под последней строкой)",
    )
    parent.focus_force()
    height = NAME.shape[0]
    width = NAME.shape[1]
    for i in range(1, height):
        for j in range(width):
            # здесь и далее состояние normal - можно писать, readonly - только чтение
            pnt[i, j].config(state="normal")
    btn = tk.Button(
        frame,
        text="OK",
        font=bt_font,
        bg=colortext,
        fg=colorback,
        command=lambda: appr_edit(
            btn, NAME, pnt, parent, root, str(path), title, coord
        ),
        width=10,
    )
    btn.grid(row=height + 1, columnspan=6)


def appr_edit(
    btn: tk.Button,
    NAME: pd.DataFrame,
    pnt: np.array,
    parent: tk.Toplevel,
    root: tk.Tk,
    path: str,
    title: str,
    coord: str,
):
    """_summary_

    Args:
        btn (tk.Button): ссылка на кнопку (чтобы удалить)
        NAME (pd.DataFrame): DataFrame
        pnt (np.array): массив указателей на виджеты Entry
        parent (tk.Toplevel): предыдущее окно (чтобы удалить его)
        root (tk.Tk): корневое окно
        path (str): путь к исходому файлу
        title (str): название окна
        coord (str): размеры окна
    """
    btn.destroy()
    height = NAME.shape[0]
    width = NAME.shape[1]
    for i in range(1, height):
        lst = []
        for j in range(width):
            pnt[i, j].config(state="readonly")
            lst.append(pnt[i, j].get())
        NAME.loc[i] = lst
    NAME.to_csv(str(path), index=False, decimal=",", sep=",")
    mb.showinfo("Успешные изменения", "Изменения успешно сохранены")
    parent.destroy()
    create_guide(root, title, coord, str(path))


def add_data(
    frame: tk.Frame,
    NAME: pd.DataFrame,
    vrs: np.array,
    pnt: np.array,
    parent: tk.Toplevel,
    root: tk.Tk,
    path: str,
    title: str,
    coord: str,
):
    """_summary_

    Args:
        frame (tk.Frame): фрейм, где находятся виджеты entry
        NAME (pd.DataFrame): DataFrame
        vrs (np.array): массив указателей на буферы
        pnt (np.array): массив указателей на виджеты Entry
        parent (tk.Toplevel): предыдущее окно (чтобы удалить его)
        root (tk.Tk): корневое окно
        path (str): путь к исходому файлу
        title (str): название окна
        coord (str): размеры окна
    """
    mb.showinfo(
        "Инструкция", "Добавьте одну запись в появившемся снизу поле и нажмите ОК"
    )
    parent.focus_force()
    height = NAME.shape[0]
    width = NAME.shape[1]
    for j in range(width):
        vrs[height, j] = tk.StringVar()
        pnt[height, j] = tk.Entry(frame, textvariable=vrs[height, j])
        pnt[height, j].grid(row=height, column=j)
        vrs[height, j].set("")
    btn = tk.Button(
        frame,
        text="OK",
        font=bt_font,
        bg=colortext,
        fg=colorback,
        command=lambda: appr_add(btn, NAME, pnt, parent, root, str(path), title, coord),
        width=10,
    )
    btn.grid(row=height + 2, columnspan=6)


def appr_add(
    btn: tk.Button,
    NAME: pd.DataFrame,
    pnt: np.array,
    parent: tk.Toplevel,
    root: tk.Tk,
    path: str,
    title: str,
    coord: str,
):
    """_summary_

    Args:
        btn (tk.Button): ссылка на кнопку (чтобы удалить)
        NAME (pd.DataFrame): DataFrame
        pnt (np.array): массив указателей на виджеты Entry
        parent (tk.Toplevel): предыдущее окно (чтобы удалить его)
        root (tk.Tk): корневое окно
        path (str): путь к исходому файлу
        title (str): название окна
        coord (str): размеры окна
    """
    height = NAME.shape[0] + 1
    width = NAME.shape[1]
    lst = []
    btn.destroy()
    # передвижение всех значений на 1 назад
    for i in range(1, height):
        for j in range(width):
            pnt[i, j].config(state="readonly")
    for j in range(width):
        lst.append(pnt[height - 1, j].get())
    NAME.loc[len(NAME.index)] = lst
    NAME.to_csv(str(path), index=False, decimal=",", sep=",")
    mb.showinfo("Успешные изменения", "Изменения успешно сохранены")
    parent.destroy()
    create_guide(root, title, coord, str(path))
