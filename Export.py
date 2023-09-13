import Database as db
import SilentErrorHandler as erh
import tkinter as tk
import pandas as pd
import os

# Export module
class Export:

    __conn = None

    __tk_window = None
    __tk_window_title = ""

    __columns_listbox = None
    __tables_listbox = None

    __db_tables = None

    __selected_table = ""
    __selected_columns = []

    __export_path = ""

    __export_formats = {
        1:"Excel",
        2:"CSV",
    }

    def __init__(self,tables,connection):
        if not connection:
            return None
        
        if not isinstance(tables, list):
            return None
        
        self.__conn = connection
        self.__tk_window_title = "Export data from database"
        self.__tk_window = tk.Tk()
        self.__db_tables = tables

    def open_window(self):
        if not self.__tk_window or not self.__conn:
            return False
        
        win = self.__tk_window
        win.title(self.__tk_window_title)
        win.geometry("800x300")

        self.__tables_listbox = tk.Listbox(win, selectmode=tk.SINGLE)
        self.__columns_listbox = tk.Listbox(win, selectmode=tk.MULTIPLE)
        self.__tables_listbox.grid(row=0, column=0, sticky="nsew")
        self.__columns_listbox.grid(row=0, column=1, sticky="nsew")

        self.__apply_columns_style()
     
        self.__display_db_tables_listbox()

        win.mainloop()


    def __display_db_tables_listbox(self):
        if not self.__tables_listbox or not self.__columns_listbox:
            return None
        
        data = self.__db_tables

        if len(data):
            window = self.__tk_window
            listbox = self.__tables_listbox

            for item in data:
                listbox.insert(tk.END, item)

            def save_selection():
                self.__selected_table = ""
                for i in listbox.curselection():
                    self.__selected_table = listbox.get(i)
                    print("Selected table: " + self.__selected_table)
                self.__insert_column_names_to_listbox()
                
            save_button = tk.Button(self.__tk_window, text="Save tables", command=save_selection)
            save_button.grid(row=2, column=0,sticky="nsew")
    
    def __insert_column_names_to_listbox(self):
        if not self.__conn:
            return False
        
        df = pd.read_sql(f"SELECT COLUMN_NAME from information_schema.columns WHERE table_name = '{self.__selected_table}'", self.__conn, columns="COLUMN_NAME")
        columns = df["COLUMN_NAME"].tolist()
       
        if len(columns):
            window = self.__tk_window
            listbox = self.__columns_listbox

            listbox.delete(0, tk.END)
            for column in columns:
                listbox.insert(tk.END, column)

            def save_selection():
                self.__selected_columns.clear()

                for i in listbox.curselection():
                    self.__selected_columns.append(listbox.get(i))

                print("Selected columns: " + str(self.__selected_columns))
                
                export_formats = self.__export_formats
                i = 0
                for key in export_formats:
                    btn_txt = f"Export {export_formats[key]}"
                    export_format_btn = tk.Button(window,text=btn_txt, command=lambda m=key: self.__export(m))
                    export_format_btn.grid(row=3,column=i, sticky="nsew")
                    i+=1

            save_button = tk.Button(window, text="Select columns", command=save_selection)
            save_button.grid(row=2,column=1,sticky="nsew")
    
    def __export(self,format):
        
        if not format:
            return None

        if format == 1:
            print(1)
        elif format == 2:
            print(2)
        else:
            return None
        
    def __apply_columns_style(self):
        window = self.__tk_window
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)


 

        
