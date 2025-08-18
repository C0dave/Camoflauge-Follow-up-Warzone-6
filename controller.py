from model import ready_data_for_table as rdft
from model import get_data, set_data
from tkinter.messagebox import *

class output_manager: 
    @staticmethod 
    def load_data_weapons(table): 
        for weapon in rdft.weapons: 
            for camo, index in zip(rdft.headers, get_data.load_weapon_index(weapon)):  
                try:
                    check_camo = list(table.item(weapon, "values")) 
                    check_camo[index] = get_data.load_weapon_camo(weapon, camo)
                    table.item(weapon, values=check_camo) 
                except KeyError: 
                    continue

    @staticmethod
    def load_weapons_and_headers(table):
        for col in table["columns"]:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=130)

        for weapon in rdft.weapons:
            table.insert("", "end", iid=weapon, values=(weapon, "", "", "", "", ""))

    @staticmethod
    def load_data_table_zip(table):
        output_manager.load_weapons_and_headers(table)
        output_manager.load_data_weapons(table)

class input_manager:
    @staticmethod
    def get_weapon_selected(table):
        weapon_selected = table.focus()
        weapon_selected = table.item(weapon_selected, "values")
        print("Arma seleccionada:", weapon_selected[0])

        return weapon_selected
    
    @staticmethod
    def add_camo(table, window, weapon_selected):
        try:
            index = sum(1 for camo in rdft.headers if camo != "Arma" if get_data.load_weapon_camo(weapon_selected[0], camo) == "✔️") + 1        
            name_camo = table['columns'][index]
            ask = askyesno("Agregar camuflaje", f"¿Ya tienes el camuflaje {name_camo} del arma {weapon_selected[0]}")
            if ask:
                add_camo_to_table = list(weapon_selected)
                add_camo_to_table[index] = "✔️"
                gold_camos = sum(1 for weapon in rdft.weapons if get_data.load_weapon_camo(weapon, "Oro") == "✔️")
                KR_camos = sum(1 for weapon in rdft.weapons if get_data.load_weapon_camo(weapon, "Rescate del Rey") == "✔️")
                if gold_camos < 7 and name_camo == "Rescate del Rey":
                    showinfo("Info", f"Tienes que desbloquear 7 camuflajes de oro en cualquier arma antes de desbloquear el camuflaje {name_camo} del arma {weapon_selected[0]}")
                elif KR_camos < 33 and name_camo == "Catalizador":
                    showinfo("Info", f"Tienes que desbloquear 33 camuflajes de Rescate del rey en todas las armas de la lista antes de desbloquear el camuflaje {name_camo} del arma {weapon_selected[0]}")
                else:
                    set_data.add_camo_to_json(weapon_selected[0], name_camo)
                    table.item(table.focus(), values=add_camo_to_table)
                    window.destroy()
            else:
                return
        except IndexError:
            showinfo("Felicitaciones", f"Felicitaciones ya tienes todos los camuflajes del arma {weapon_selected[0]}")
    
    @staticmethod
    def del_camo(table, window, weapon_selected):
        index = sum(1 for camo in rdft.headers if camo != "Arma" if get_data.load_weapon_camo(weapon_selected[0], camo) == "✔️")        
        name_camo = table['columns'][index]
        if index < 1:
            showinfo("Info", "No hay camuflajes para eliminar")
            return
        else:
            ask = askyesno("Eliminar camuflaje", f"¿Quieres eliminar el camuflaje {name_camo} del arma {weapon_selected[0]}")
            if ask:
                set_data.del_camo_from_json(weapon_selected[0], name_camo, index)
                del_camo_from_table = list(weapon_selected)
                del_camo_from_table[index] = ""
                table.item(table.focus(), values=del_camo_from_table)
                window.destroy()
      