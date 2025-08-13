from ttkbootstrap import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
from data_manager import *
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main_window():
    global table
    try:
        with open("weapons_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        showerror("Error", "Archivo JSON no existe (Cierra este mensaje para crearlo)")
        create_json_file()
        return
    window = Window(themename="darkly")
    window.title("Seguimiento de camuflajes de Warzone")
    window.geometry("850x590")
    window.iconbitmap(resource_path("images/icon.ico"))
    window.resizable(False, False)

    show_camos_statistics()

    style = Style()
    style.configure("Treeview", rowheight=40, font=("Arial", 15))

    image = Image.open(resource_path("images/image.png"))
    image = image.resize((60, 35))
    tk_image = ImageTk.PhotoImage(image)

    image2 = Image.open(resource_path("images/image2.png"))
    image2 = image2.resize((100, 35))
    tk_image2 = ImageTk.PhotoImage(image2)

    image_label = Label(window, image=tk_image)
    image_label.place(x=40, y=450)

    intermediate_bar = Label(window, text="|", font=("Arial", 24))
    intermediate_bar.place(x=115, y=447)

    image_label2 = Label(window, image=tk_image2)
    image_label2.place(x=133, y=450)

    welcome_label = Label(window, text="Hola, Alejandro", font=("Arial", 24))
    welcome_label.place(x=40, y=40)

    table = Treeview(window, columns=("Arma", "Militar", "Especial", "Oro", "Rescate del Rey", "Catalizador"), show="headings")
    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=130)
        
    for weapon in weapons:
        table.insert("", "end", values=(weapon, data[weapon]["Militar"], data[weapon]["Especial"], data[weapon]["Oro"], data[weapon]["Rescate del Rey"], data[weapon]["Catalizador"]))

    table.pack(pady=155)
    table.bind("<ButtonRelease-1>", lambda event: take_decision(table))

    window.mainloop()

if __name__ == "__main__":
    main_window()