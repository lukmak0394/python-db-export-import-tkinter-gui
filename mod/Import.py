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

    __import_extensions = {
        1:".csv",
    }
    __import_folder = ""

    __files_list_listbox = None

    __selected_file = ""

    def __init__(self):
        super().__init__()
        load_dotenv()
        self.__import_folder = os.getenv("import_folder")
        super()._create_folder(self.__import_folder,"creating import folder...")


    def open_window(self):
        super()._open_root_window("Import")
    
    def _save_columns(self):
        super()._save_columns()
        self.__open_uploader()

    def __open_uploader(self):
        super()._open_top_window("Upload file", "550x250")

        top = self._top_level_window
        top.columnconfigure(0, weight=1)
        upload_new_btn = Button(top,text="Upload new file",command=self.__upload_new,bg="#0d6efd", fg="white")
        upload_new_btn.grid(column=0,row=1, columnspan=2,sticky="nsew")

        self.__files_list_listbox = Listbox(top, selectmode=SINGLE)
        self.__files_list_listbox.grid(column=0,row=2, columnspan=2, sticky="nsew")

        date = super()._get_date()
        def save_selection():
            try:
                file_list = self.__files_list_listbox
                selection = file_list.curselection()
                file = file_list.get(selection[0])
                self.__selected_file = os.path.join(self.__import_folder,file)
                print(self.__selected_file)
            except (TypeError, AttributeError, Exception) as e:
                erh.SilentErrorHandler.log_error(f"{str(e)}")
                print(f"{date} - Something went wrong, try again")

        upload_new_btn = Button(top,text="Import",command=save_selection,bg="#0d6efd", fg="white")
        upload_new_btn.grid(column=0,row=3, columnspan=2,sticky="nsew")

        self.__show_existing_files()

        top.mainloop()

    def __show_existing_files(self):
        files_list = self.__files_list_listbox
        import_folder = self.__import_folder
        import_formats = self.__import_extensions

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
        for key, file_ext in self.__import_extensions.items():
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




        
