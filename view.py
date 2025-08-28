from ttkbootstrap import *
from controller import output_manager, input_manager
from PIL import Image, ImageTk
from model import Weapons_and_Headers as WaH
import sys, os

class image: 
    @staticmethod
    def take_image(image_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, image_path)

    @staticmethod
    def set_image_style(window, x, y, width, height, image_path):
        image_opened = Image.open(image_path)
        image_opened = image_opened.resize((width, height)) 
        ready_image = ImageTk.PhotoImage(image_opened)

        return_image = Label(window, image=ready_image)
        return_image.image = ready_image  
        return_image.place(x=x, y=y) 

        return return_image
    
class windows:
    @staticmethod
    def Main_window():
        global table
        main_window = Window(themename="darkly")
        main_window.title("Seguimiento de camuflajes de Warzone")
        main_window.geometry("850x590")
        main_window.iconbitmap(image.take_image("images/icon.ico"))
        main_window.resizable(False, False)

        welcome_label = Label(main_window, text="Hola, Alejandro", font=("Arial", 24))
        welcome_label.place(x=40, y=40)
 
        table_style = Style()
        table_style.configure("Treeview", rowheight=40, font=("Arial", 15))
        table = Treeview(main_window, columns=(WaH.headers), cursor="hand2", show="headings")
        output_manager.load_data_table_zip(table)
        table.tag_configure("category", background="#032E4B", foreground="white", font=("Arial", 9, "bold"))
        table.tag_bind("category", "<ButtonRelease-1>", lambda e: table.selection_remove(table.focus()))
        table.bind("<ButtonRelease-1>", lambda e: windows.Question_window(input_manager.get_weapon_selected(table)))
        table.pack(pady=155, expand=True, fill="both")
 
        image.set_image_style(main_window, 40, 450, 60, 35, image.take_image("images/image.png"))
        separator_bar = Label(main_window, text="|", font=("Arial", 24))
        separator_bar.place(x=115, y=447)
        image.set_image_style(main_window, 133, 450, 100, 35, image.take_image("images/image2.png"))

        main_window.mainloop()
    
    @staticmethod
    def Question_window(weapon_selected):
        if weapon_selected != None:
            window = Toplevel()
            window.title("Decisión de camuflaje")
            window.geometry("300x200")
            window.iconbitmap(image.take_image("images/icon.ico"))
            window.resizable(False, False)
            
            weapon_selected_label = Label(window, text=f"Arma seleccionada {weapon_selected}", font=("Arial", 12, "bold"))
            weapon_selected_label.pack(pady=10)

            question_label = Label(window, text=f"¿Que vas a hacer?", font=("Arial", 10, "bold"))
            question_label.pack()

            button_add = Button(window, text="Agregar camuflaje", style="success", cursor="hand2",command=lambda: input_manager.add_camo(table, window, weapon_selected))
            button_add.pack(pady=15)

            button_delete = Button(window, text="Eliminar camuflaje", style="danger", cursor="hand2", command=lambda: input_manager.del_camo(table, window, weapon_selected))
            button_delete.pack() 

            window.grab_set()
