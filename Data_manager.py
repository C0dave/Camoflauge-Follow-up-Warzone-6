from ttkbootstrap import *
from tkinter.messagebox import *
import json
from main import resource_path 

weapons = [
    "XM4",
    "AK-74",
    "Ames-85",
    "GPR-91",
    "Model-L",
    "Goblin-MK2",
    "AS-VAL",
    "Krig-C",
    "Cypher-091",
    "Kilo-141",
    "CR-56-AMAX",
    "FFAR-1",
    "C9",
    "KSV",
    "Tanto-.22",
    "PP-919",
    "Jackal-PDW",
    "Kompakt-92",
    "Saug",
    "PPSH-41",
    "LC10",
    "Ladra",
    "Marine-SP",
    "ASG-89",
    "Maelstrom",
    "PU-21",
    "XMG",
    "GPMG-7",
    "Feng-82",
    "SWAT-5.56",
    "DM-10",
    "TR2"
]

@staticmethod
def create_json_file():
    headings = ["Militar", "Especial", "Oro", "Rescate del Rey", "Catalizador"]
    weapons_data = {weapon: {camo: "" for camo in headings} | {"index_table": 1} for weapon in weapons}
    with open("weapons_data.json", "w", encoding="utf-8") as file:
        json.dump(weapons_data, file, indent=4, ensure_ascii=False)

@staticmethod
def show_camos_statistics():
    with open("weapons_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        num_military_camos = sum(1 for weapon in data if data[weapon]["Militar"] == "✔️")
        num_especial_camos = sum(1 for weapon in data if data[weapon]["Especial"] == "✔️")
        num_gold_camos = sum(1 for weapon in data if data[weapon]["Oro"] == "✔️")
        num_king_rescue_camos = sum(1 for weapon in data if data[weapon]["Rescate del Rey"] == "✔️")
        num_catalizador_camos = sum(1 for weapon in data if data[weapon]["Catalizador"] == "✔️")
        statistics_label = Label(text=f"Camuflajes Militares: {num_military_camos}\nCamuflajes Especiales: {num_especial_camos}\nCamuflajes Oro: {num_gold_camos}\nCamuflajes Rescate del Rey: {num_king_rescue_camos}\nCamuflajes Catalizador: {num_catalizador_camos}", font=("Arial", 16))
        statistics_label.pack(pady=20)
        statistics_label.place(x=550, y=20)

@staticmethod
def take_decision(table):
    window = Toplevel()
    window.title("Decisión de camuflaje")
    window.geometry("300x200")
    window.iconbitmap(resource_path("images/icon.ico"))
    window.resizable(False, False)
    
    question_label = Label(window, text=f"Que vas a hacer?")
    question_label.pack(pady=10)

    button_delete = Button(window, text="Eliminar camuflaje", command=lambda: delete_camo(table, window))
    button_delete.pack(pady=10) 

    button_add = Button(window, text="Agregar camuflaje", command=lambda: add_camo(table, window))
    button_add.pack(pady=10)

    window.grab_set()

@staticmethod
def add_camo(table, window):
    weapon_selected = table.focus()
    with open("weapons_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        try:
            if weapon_selected:
                weapon_selected = table.item(weapon_selected, "values")
                index = data[weapon_selected[0]]["index_table"]
                name_camo = table['columns'][index]
                print(f"Arma seleccionada: {weapon_selected[0]}")
                ask = askyesno("Agregar camuflaje", f"¿Ya tienes el camuflaje {name_camo} del arma {weapon_selected[0]}?", parent=window)
                if ask:
                    num_gold_camos = sum(1 for weapon in data if data[weapon]["Oro"] == "✔️")
                    num_king_rescue_camos = sum(1 for weapon in data if data[weapon]["Rescate del Rey"] == "✔️")
                    if num_gold_camos < 7 and name_camo == "Rescate del Rey":
                        showinfo("Info", f"Tienes que desbloquear 7 camuflajes de oro en cualquier arma antes de desbloquear el camuflaje {name_camo} del arma {weapon_selected[0]}")
                    elif num_king_rescue_camos < 33 and name_camo == "Catalizador":
                        showinfo("Info", f"Tienes que desbloquear 33 camuflajes de Rescate del rey en todas las armas de la lista antes de desbloquear el camuflaje {name_camo} del arma {weapon_selected[0]}")
                    else:
                        data[weapon_selected[0]]["index_table"] += 1
                        data[weapon_selected[0]][name_camo] = "✔️"
                        check_camos = list(weapon_selected)
                        check_camos[index] = "✔️"
                        table.item(table.focus(), value=check_camos)
                else:
                    return
                with open("weapons_data.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                show_camos_statistics()
        except IndexError:
            showinfo("Felicitaciones", f"Ya tienes todos los camuflajes de el arma {weapon_selected[0]} desbloqueados")
    window.destroy()

@staticmethod
def delete_camo(table, window):
    weapon_selected = table.focus()
    with open("weapons_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if weapon_selected:
            weapon_selected = table.item(weapon_selected, "values")
            index = data[weapon_selected[0]]["index_table"]
            if index <= 1:
                showinfo("Info", "No hay camuflajes para eliminar.")
                return
            else:
                last_camo = table['columns'][index - 1]
                ask = askyesno("Eliminar camuflaje", f"¿Quieres eliminar el camuflaje de {last_camo} {weapon_selected[0]}?", parent=window)
                if ask:
                    data[weapon_selected[0]][last_camo] = ""
                else:
                    return
                data[weapon_selected[0]]["index_table"] -= 1
                check_camos = list(weapon_selected)
                check_camos[index - 1] = ""
                table.item(table.focus(), value=check_camos)
                with open("weapons_data.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                show_camos_statistics()
                window.destroy()