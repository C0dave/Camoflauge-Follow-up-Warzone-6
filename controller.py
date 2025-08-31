from model import Weapons_and_Headers as WaH
from model import get_data, set_data
from tkinter.messagebox import *


class requirements:
    @staticmethod
    def min_num_gold_camos(category_weapon, name_camo, delete:bool) -> bool:
        if delete:
            check_gold_camos = bool(get_data.get_num_camos(category_weapon, "gold_camos", True) <= get_data.get_min_num_camos(category_weapon))
            check_name_camo = bool(name_camo == "Oro" and check_gold_camos)
            return check_name_camo
        else:
            check_gold_camos = bool(get_data.get_num_camos(category_weapon, "gold_camos", True) < get_data.get_min_num_camos(category_weapon) and name_camo == "Rescate del Rey")
            return check_gold_camos

    @staticmethod
    def min_num_KR_camos(category_weapon, name_camo, delete:bool) -> bool:
        if delete:
            check_KR_camos = bool(get_data.get_num_camos(None, "Total_KR_camos", False) <= 33)
            check_name_camo = bool(name_camo == "Rescate del Rey" and check_KR_camos)
            return check_name_camo
        else:
            check_KR_camos = bool(get_data.get_num_camos(category_weapon, "KR_camos", True) < 33 and name_camo == "Catalizador")
            return check_KR_camos
    
class output_manager: 
    @staticmethod  
    def show_data_weapons(table): 
        for category in WaH.weapon_categories:
            for weapon in getattr(WaH, category): 
                for camo, index in zip(WaH.headers, get_data.get_weapon_index()):  
                    try:
                        check_camo = list(table.item(weapon, "values")) 
                        check_camo[index] = get_data.get_weapon_camo(category, weapon, camo)
                        table.item(weapon, values=check_camo) 
                    except KeyError: 
                        continue

    @staticmethod
    def show_weapons_and_headers(table):
        for col in table["columns"]: 
            table.heading(col, text=col)
            table.column(col, anchor="center", width=140)

        for category, category_ES in zip(WaH.weapon_categories, WaH.weapon_categories_ES_title):
            table.insert("", "end", values=("", "", category_ES), tags=("category",))
            for weapon in getattr(WaH, category): 
                table.insert("", "end", iid=weapon, values=(weapon, "", "", "", "", ""))

    @staticmethod
    def show_weapon_category(weapon):
        for category in WaH.weapon_categories:
            if weapon in getattr(WaH, category):
                return category
            else:
                continue
    
    @staticmethod
    def show_weapon_category_ES(weapon):
        for num, category in enumerate(WaH.weapon_categories):
            if weapon in getattr(WaH, category):
                return WaH.weapon_categories_ES[num]
            else:
                continue
    
    @staticmethod
    def show_num_KR_camos():
        for category in WaH.weapon_categories:
            num_KR_camo = sum(get_data.load_num_KR_camos(category))
            return num_KR_camo                

    @staticmethod
    def show_data_table_zip(table):
        output_manager.show_weapons_and_headers(table)
        output_manager.show_data_weapons(table)

class input_manager:
    @staticmethod
    def get_weapon_selected(table):
        weapon_selected = table.focus()
        weapon_selected = table.item(weapon_selected, "values")[0]
        if weapon_selected != "":
            print("Arma seleccionada:", weapon_selected)
            return weapon_selected
        
    @staticmethod
    def add_camo(table, window, weapon_selected):
        try:
            one_category = output_manager.show_weapon_category(weapon_selected)
            index = sum(1 for camo in WaH.headers if camo != "Arma" if get_data.get_weapon_camo(one_category, weapon_selected, camo) == "✔️") + 1
            name_camo = table['columns'][index]
            ask = askyesno("Agregar camuflaje", f"¿Ya tienes el camuflaje {name_camo} del arma {weapon_selected}", parent=window)
            if ask:
                if not requirements.min_num_gold_camos(one_category, name_camo, False):
                    if requirements.min_num_KR_camos(one_category, name_camo, False):
                        showinfo("info", f"Debes desbloquear todos los camuflajes todos los rescates del rey en todas para desbloquear el camuflaje catalizador del arma {weapon_selected}", parent=window)
                        return
                    
                    if name_camo == "Oro":
                        set_data.add_num_camo_to_json(one_category, "gold_camos", True)
                    elif name_camo == "Rescate del Rey":
                        set_data.add_num_camo_to_json(one_category, "KR_camos", True)
                        set_data.add_num_camo_to_json(None, "Total_KR_camos", False)
                    elif name_camo == "Catalizador":
                        set_data.add_num_camo_to_json(None, "Catalyst_camos", False)
                    set_data.add_camo_to_json(one_category, weapon_selected, name_camo)                    
                    output_manager.show_data_weapons(table)                        
                else:
                    showinfo("info", f"Debes desbloquear {get_data.get_min_num_camos(one_category)} de camuflajes oro en cualquier {output_manager.show_weapon_category_ES(weapon_selected)} para desbloquear el rescate del rey del arma {weapon_selected}", parent=window)
            else:
                return
            window.destroy()
        except IndexError:
            showinfo("Felicitaciones", f"Felicitaciones ya tienes todos los camuflajes del arma {weapon_selected}", parent=window)
        
    @staticmethod
    def del_camo(table, window, weapon_selected):
        one_category = output_manager.show_weapon_category(weapon_selected)
        index = sum(1 for camo in WaH.headers if camo != "Arma" if get_data.get_weapon_camo(one_category, weapon_selected, camo) == "✔️")        
        name_camo = table['columns'][index] 
        question_1 = askyesno("Eliminar camuflaje", f"¿Quieres eliminar el camuflaje {name_camo} del arma {weapon_selected}", parent=window)
        if question_1:
            if index < 1:
                showerror("Error", f"No hay camuflajes para eliminar del arma {weapon_selected}", parent=window)
                return
            else:
                if requirements.min_num_gold_camos(one_category, name_camo, True) and get_data.get_num_camos(one_category, "KR_camos", True) > 1:
                    question_2 = askyesno("Advertencia", f"Si eliminas el camuflaje de oro del arma {weapon_selected} se eliminaran tambien todos los camuflajes de rescate del rey que tengas en la categoria {output_manager.show_weapon_category_ES(weapon_selected)}, porque ya no tienes la cantidad minima de camuflajes de oro para agregar camuflajes de rescate del rey. ¿Quieres eliminar el camuflaje de oro del arma {weapon_selected}?", parent=window)
                    if question_2:
                        set_data.del_num_camo_from_json(one_category, "KR_camos", True, True)
                        for weapon in getattr(WaH, one_category):
                            set_data.del_camo_from_json(one_category, weapon, "Rescate del Rey")
                        output_manager.show_data_weapons(table)
                    else:
                        return
                if requirements.min_num_KR_camos(one_category, name_camo, True) and get_data.get_num_camos(None, "Catalyst_camos", False) > 0:
                    question_3 = askyesno("Advertencia", f"Si eliminas el camuflaje de rescate del rey del arma {weapon_selected}, tambien se borraran todos los camuflajes de catalizador en todas las armas, porque ya no tienes todos los camuflajes de rescate del rey. ¿Quieres eliminar el camuflaje de rescate del rey del arma {weapon_selected}?", parent=window)
                    if question_3:
                        set_data.del_num_camo_from_json(None, "Catalyst", False, True)
                        for all_categories in WaH.weapon_categories:
                            for weapon in getattr(WaH, all_categories):
                                set_data.del_camo_from_json(all_categories, weapon, "Catalizador")
                        output_manager.show_data_weapons(table)
                    else:
                        return
                
                if name_camo == "Oro":
                    set_data.del_num_camo_from_json(one_category, "gold_camos", True, False)
                elif name_camo == "Rescate del Rey":
                    set_data.del_num_camo_from_json(one_category, "KR_camos", True, False)
                    set_data.del_num_camo_from_json(None, "Total_camos", False, False)
                elif name_camo == "Catalizador":
                    set_data.del_num_camo_from_json(one_category, "KR_camos", True, False)
                set_data.del_camo_from_json(one_category, weapon_selected, name_camo)
                output_manager.show_data_weapons(table)
            window.destroy()
        else:
            return      