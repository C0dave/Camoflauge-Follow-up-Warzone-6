from ttkbootstrap import *
from tkinter.messagebox import *
from Data_manager import *
import os

def main_window():
    if not os.path.exists("weapons_data.json"):
        create_json_file()
    global table
    with open("weapons_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    window = Window(themename="darkly")
    window.title("Seguimiento de camuflajes de Warzone")
    window.geometry("850x650")
    window.resizable(False, False)

    show_camos_statistics()

    style = Style()
    style.configure("Treeview", rowheight=40, font=("Arial", 15))

    welcome_label = Label(window, text="Hola, Alejandro", font=("Arial", 24))
    welcome_label.place(x=30, y=20)

    table = Treeview(window, columns=("Arma", "Militar", "Especial", "Oro", "Rescate del Rey", "Catalizador"), show="headings")
    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=130)
        
    for weapon in weapons:
        table.insert("", "end", values=(weapon, data[weapon]["Militar"], data[weapon]["Especial"], data[weapon]["Oro"], data[weapon]["Rescate del Rey"], data[weapon]["Catalizador"]))

    table.pack(pady=180, padx=20)
    table.bind("<ButtonRelease-1>", lambda event: take_decision(event, table))

    window.mainloop()

if __name__ == "__main__":
    main_window()