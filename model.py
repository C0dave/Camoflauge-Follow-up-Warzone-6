from tkinter.messagebox import *
import json
import os
import sys

class Weapons_and_Headers:
    Assault_rifles = ["XM4", "AK-74", "Ames-85", "GPR-91", "Model-L", "Goblin-MK2", "AS-VAL", "Krig-C", "Cypher-091", "Kilo-141", "CR-56-AMAX", "FFAR-1"]
    Submachine_guns = ["C9", "KSV", "Tanto-.22", "PP-919", "Jackal-PDW", "Kompakt-92", "Saug", "PPSH-41", "LC10", "Ladra"]
    Shotguns = ["Marine-SP", "ASG-89", "Maelstrom"]
    Light_machine_guns = ["PU-21", "XMG", "GPMG-7", "Feng-82"]
    Marksman_rifles = ["SWAT-5.56", "DM-10", "TR2"]
    headers = ["Arma", "Militar", "Especial", "Oro", "Rescate del Rey", "Catalizador"] 
    weapon_categories = ["Assault_rifles", "Submachine_guns", "Shotguns", "Light_machine_guns", "Marksman_rifles"]
    weapon_categories_ES_title = ["Rifles de asalto", "Subfusiles", "Escopetas", "Ametralladoras ligeras", "Fusiles tacticos"]
    weapon_categories_ES = ["rifle de asalto", "subfusil", "escopeta", "ametralladora ligera", "fusil tactico"]

class get_data:
    @staticmethod
    def get_weapon_index() -> int:
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                index_data = data["index_table"]
            return index_data
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no exite cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)

    @staticmethod
    def get_weapon_camo(category_weapon:str, weapon:str, camo:str) -> str:
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                camo_data = data[category_weapon][weapon][camo]
            return camo_data
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no exite cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)
    
    @staticmethod
    def get_min_num_camos(category_weapon:str) -> int:
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                num_gold_camos = data[category_weapon]["minimum_gold_camos"]
            return num_gold_camos
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no exite cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)
    
    @staticmethod
    def get_num_camos(category_weapon:str, camo:str, in_category:bool) -> int:
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                num_of_camos = None
                if in_category:
                    num_of_camos = data[category_weapon][camo]
                else:
                    num_of_camos = data[camo]
            return num_of_camos
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no exite cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)
    
class set_data:
    @staticmethod
    def create_json_file() -> json:
        WaH = Weapons_and_Headers 
        if not os.path.exists("weapons_data.json"):
            headings = ["Militar", "Especial", "Oro", "Rescate del Rey", "Catalizador"]
            min_gold_camos = [7, 6, 2, 3, 3]
            weapons_data = {category: {**{weapon: {camo: "" for camo in headings} for weapon in getattr(WaH, category)}} | {"minimum_gold_camos": min_gold_camos[num]} | {"gold_camos": 0, "KR_camos": 1} for category, num in zip(WaH.weapon_categories, range(5))} | {"index_table": list(range(6)), "Total_KR_camos": 1, "Catalyst_camos": 1}
            with open("weapons_data.json", "w", encoding="utf-8") as file:
                json.dump(weapons_data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def add_camo_to_json(category_weapon:str, weapon:str, camo:str):
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                data[category_weapon][weapon][camo] = "✔️"
            with open("weapons_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no existe. Cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)

    @staticmethod
    def add_num_camo_to_json(category_weapon:str, camo:str, in_category:bool):
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if in_category:
                    data[category_weapon][camo] += 1
                else:
                    data[camo] += 1
            with open("weapons_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)        
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no existe. Cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)

    @staticmethod
    def del_camo_from_json(category_weapon:str, weapon:str, camo:str):
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                data[category_weapon][weapon][camo] = ""
            with open("weapons_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)        
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no existe. Cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0)

    @staticmethod
    def del_num_camo_from_json(category_weapon:str, camo:str, in_category:bool, all:bool):
        try:
            with open("weapons_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if in_category:
                    if all:
                        data[category_weapon][camo] = 1
                    else:
                        data[category_weapon][camo] -= 1
                else:
                    if all:
                        data[camo] = 1
                    else:
                        data[camo] -= 1
            with open("weapons_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)        
        except FileNotFoundError:
            showerror("Error", "Carpeta JSON no existe. Cierra el mensaje para crearlo")
            set_data.create_json_file()
            sys.exit(0) 