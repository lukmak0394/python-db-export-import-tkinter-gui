import os
import pandas as pd
from tkinter import *
from tkinter import filedialog
import datetime
from dotenv import load_dotenv
import SilentErrorHandler as erh
import shutil


class Import:

    __root_import_window = None

    __import_formats = {
        1:".xlsx",
        2:".csv",
    }

    __import_folder = ""

    __files_list_listbox = None

    __selected_file = ""

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

        date = self.__get_date()
        def save_selection():
            try:
                file_list = self.__files_list_listbox
                selection = file_list.curselection()
                file = file_list.get(selection[0])
                f_path = os.path.join(self.__import_folder,file)
                df = pd.read_excel(f_path)
                print(df)
            except (TypeError, AttributeError, Exception) as e:
                print(f"{date} - Something went wrong, try again")
                erh.SilentErrorHandler.log_error(f"{str(e)}")
 

        upload_new_btn = Button(win,text="Read selected file",command=save_selection,bg="#0d6efd", fg="white")
        upload_new_btn.grid(column=0,row=4, columnspan=2,sticky="nsew")

        self.__show_existing_files()

        win.mainloop()
        return True


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
        date = self.__get_date()
        import_folder = self.__import_folder

        xslx_ext = self.__import_formats[1]
        csv_ext = self.__import_formats[2]

        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", f"*{csv_ext}"), ("Excel Files", f"*{xslx_ext}")])
        if file_path:
            try:
                dest = os.path.join(import_folder,os.path.basename(file_path))
                shutil.move(file_path, dest)
                print(f"{date} = moved file: {file_path} to {dest}")
                self.__show_existing_files()  
            except (TypeError, AttributeError, Exception) as e:
                print(f"{date} - Something went wrong, try again")
                erh.SilentErrorHandler.log_error(f"{str(e)}")
    

    def __create_import_folder(self):
        if not os.path.exists(self.__import_folder):
            date = self.__get_date()
            print(f"{date} - creating import folder...")
            os.mkdir(self.__import_folder)

    def __sanitize_string(self,txt):
        txt = str(txt)
        txt = txt.replace("DROP"," ")
        txt = txt.replace("DELETE"," ")
        txt = txt.replace("UPDATE"," ")
        txt = txt.replace(";"," ")
        txt = txt.replace("`", " ")
        txt = txt.replace("\""," ")
        return txt

    def __get_date(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        return date
        