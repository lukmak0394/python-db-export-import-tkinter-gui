import Database as db
import SilentErrorHandler as erh
import tkinter as tk
import pandas as pd

# Export module
class Export:

    __conn = None

    __tk_window = None
    __tk_window_title = ""

    __tables_data = None

    __selected_table = ""
    __selected_columns = []

    __export_format = None
    __export_path = ""
    __export_formats = {
        1:"Excel",
        2:"CSV",
    }

    def __init__(self,tables, connection):
        if not connection:
            return None
        
        if not isinstance(tables, list):
            return None
        
        self.__conn = connection
        self.__tk_window_title = "Export data from database"
        self.__tk_window = tk.Tk()
        self.__tables_data = tables

    def __append_db_tables_listbox(self,tables_listbox,columns_listbox,data):
        if not type(data) is list:
            return False
        
        if len(data):
            
            for item in data:
                tables_listbox.insert(tk.END, item)

            def save_selection():
                self.__selected_table = ""
                for i in tables_listbox.curselection():
                    self.__selected_table = tables_listbox.get(i)
                    print("Table selected: " + self.__selected_table)

                self.__append_tables_columns_listbox(columns_listbox)
                
            save_button = tk.Button(self.__tk_window, text="Submit", command=save_selection)
            save_button.grid(row=2, column=0,sticky="nsew")
    
    def __append_tables_columns_listbox(self,listbox):
        if not self.__tk_window:
            return False
        
        df = pd.read_sql(f"SELECT COLUMN_NAME from information_schema.columns WHERE table_name = '{self.__selected_table}'", self.__conn, columns="COLUMN_NAME")
        columns = df["COLUMN_NAME"].tolist()
       
        if len(columns):

            listbox.delete(0, tk.END)

            for column in columns:
                listbox.insert(tk.END, column)

            def save_selection():
                self.__selected_columns.clear()
                for i in listbox.curselection():
                    self.__selected_columns.append(listbox.get(i))
                print("Columns selected: " + str(self.__selected_columns))
               
                i = 0
                for key in self.__export_formats:
                    export_format_btn = tk.Button(self.__tk_window,text=self.__export_formats[key], command=lambda m=key: self.__set_format(m))
                    export_format_btn.grid(row=3,column=i, sticky="nsew")
                    i+=1

            save_button = tk.Button(self.__tk_window, text="Select columns", command=save_selection)
            save_button.grid(row=2,column=1,sticky="nsew")
    
    def __set_format(self,format):
        
        if not format:
            return False

        if format == 1:
            self.__export_format = 1
        elif format == 2:
            self.__export_format = 2
        elif format == 3:
            self.__export_format = 3
        else:
            return None
        
        if self.__selected_columns and self.__selected_table and self.__export_format:
            print(f"Selected format: {self.__export_formats[self.__export_format]}")
            self.__display_export_btn()

    def __display_export_btn(self):
        if not self.__tk_window:
            return False
        
        query = "SELECT "
        for column in self.__selected_columns:
            query += column + ", "  # Add the column to the query string

        query = query.rstrip(", ")
        query += f" FROM {self.__selected_table}"
        
        excel_file = f"{self.__selected_table}.xlsx"
        def export():
            if self.__export_format == 1:
                df = pd.read_sql(f"{query}", self.__conn)
                df.to_excel(excel_file)
            
        
        export_btn = tk.Button(self.__tk_window, text="Export data!", command=export)
        export_btn.grid(row=4,column=0, sticky="nsew")

    def __format_columns_style(self,window):
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)

    def initialize(self):
        if not self.__tk_window:
            return False
        
        win = self.__tk_window
        win.title(self.__tk_window_title)
        win.geometry("800x300")

        db_tables_listbox = tk.Listbox(win, selectmode=tk.SINGLE)
        table_columns_listbox = tk.Listbox(win, selectmode=tk.MULTIPLE)
        
        db_tables_listbox.grid(row=0, column=0, sticky="nsew")
        table_columns_listbox.grid(row=0, column=1, sticky="nsew")

        self.__format_columns_style(win)
     
        self.__append_db_tables_listbox(db_tables_listbox,table_columns_listbox,self.__tables_data)
            
        win.mainloop()
         


    

 

        
