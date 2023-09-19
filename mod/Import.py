import os
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from dotenv import load_dotenv
import shutil
import mod.Module as core
import SilentErrorHandler as erh

class Import(core.Module):

    __root_import_window = None
    __top_level_window = None

    __import_formats = {
        1:".xlsx",
        2:".csv",
    }
    __import_folder = ""

    __files_list_listbox = None

    __selected_file = ""

    # 1 xlsx 2 csv
    __import_type = None

    def __init__(self):
        load_dotenv()
        self.__import_folder = os.getenv("import_folder")
        self.__create_import_folder()
    

    def open_import_window(self):
        self.__root_import_window = Tk()
        self.__root_import_window.title("Import")
        self.__root_import_window.geometry("300x300")
        
        if not self.__root_import_window:
            return False
        
        if not self.__import_formats or not self.__import_folder:
            return False
        
        win = self.__root_import_window

        win.columnconfigure(0, weight=1)

        upload_new_btn = Button(win,text="Upload new file",command=self.__upload_new,bg="#0d6efd", fg="white")
        upload_new_btn.grid(column=0,row=2, columnspan=2,sticky="nsew")

        self.__files_list_listbox = Listbox(win, selectmode=SINGLE)
        self.__files_list_listbox.grid(column=0,row=3, columnspan=2, sticky="nsew")

        date = super()._get_date()
        def save_selection():
            try:
                file_list = self.__files_list_listbox
                selection = file_list.curselection()
                file = file_list.get(selection[0])
                f_path = os.path.join(self.__import_folder,file)
                df = pd.read_excel(f_path)
                self.__open_import_settings()
            except (TypeError, AttributeError, Exception) as e:
                erh.SilentErrorHandler.log_error(f"{str(e)}")
                print(f"{date} - Something went wrong, try again")

 

        upload_new_btn = Button(win,text="Read selected file",command=save_selection,bg="#0d6efd", fg="white")
        upload_new_btn.grid(column=0,row=4, columnspan=2,sticky="nsew")

        self.__show_existing_files()

        win.mainloop()
        return True

    def __open_import_settings(self):
        refresh = False

        if not self.__top_level_window:
            top = Toplevel(self.__root_import_window)
            self.__top_level_window = top
        else:
            refresh = True
            top = self.__top_level_window
            top.update()
            top.update_idletasks()
        
        top.title("Import settings")
        top.geometry("600x300")

        import_options = ["INSERT", "UPDATE"]
        import_type_label = Label(top, text="Select import type")
        import_type_label.grid(row=0, column=0, sticky="nsew")
        import_type  = StringVar()
        import_type_select = ttk.Combobox(top, textvariable=import_type, values=import_options, state="readonly")
        import_type_select.grid(row=0,column=1, sticky="nsew")

        def save_selection():
            type = import_type.get()
            if len(type) == 0:
                print("Type not selected")
                return False
            if type.upper() == "INSERT":
                self.__import_type = 1
            else:
                self.__import_type = 2



        save_button = Button(top, text="Save", command=save_selection, bg="#0d6efd", fg="white")
        save_button.grid(row=0, column=2, columnspan=2, sticky="nsew")



    def __show_existing_files(self):
        files_list = self.__files_list_listbox
        import_folder = self.__import_folder
        import_formats = self.__import_formats

        if not files_list:
            return False
        
        files_list.delete(0,END)
        for filename in os.listdir(import_folder):
            for key, format in import_formats.items():
                if filename.endswith(f"{format}"):
                    files_list.insert(END, filename)

        return True

    def __upload_new(self):
        date = super()._get_date()
        import_folder = self.__import_folder

        filetypes = []
        for key, file_ext in self.__import_formats.items():
            filetypes.append((f"File types", f"*{file_ext}"))
            
        file_path = filedialog.askopenfilename(filetypes=filetypes, multiple=True)
        if file_path:
            try:
                for file in file_path:
                    dest = os.path.join(import_folder,os.path.basename(file))
                    shutil.copy(file,dest)
                    super()._print_user_message(f"moved file: {file} to {dest}")
                self.__show_existing_files()  
            except (TypeError, AttributeError, Exception) as e:
                print(f"{date} - Something went wrong, try again")
                super()._print_user_message("Something went wrong, try again")
                erh.SilentErrorHandler.log_error(f"{str(e)}")
    
    def __create_import_folder(self):
        date = super()._get_date()
        super()._create_folder(self.__import_folder,"creating import folder...")


        
