import os
import pandas as pd
import datetime
import SilentErrorHandler as erh
import sqlalchemy.exc as sqe
import Database as db
from tkinter import *

class Module():

    _conn = None
    _root_win = None
    _top_level_window = None
    __tables_listbox = None
    __columns_listbox = None

    _db_tables = []
    _db_tab_columns = []

    _selected_table = ""
    _selected_columns = []

    _refresh = False

    def __init__(self):
        connection =  db.Database().connect()
        self._conn = connection
        tables = db.Database().get_tables(connection)
        if not isinstance(tables, list):
            return None
        self._db_tables = tables
    
    def _open_root_window(self,title):
        if not self._conn:
            return False
        
        self._root_win = Tk()
        root = self._root_win
        root.title(title)
        root.geometry("800x300")

        label_tables = Label(root, text="Database tables")
        label_tables.grid(row=1, column=0, sticky="nsew")
        label_columns = Label(root, text="Columns to select")
        label_columns.grid(row=1, column=1, sticky="nsew")

        self.__tables_listbox = Listbox(root, selectmode=SINGLE)
        self.__columns_listbox = Listbox(root, selectmode=MULTIPLE)
        self.__tables_listbox.grid(row=2, column=0, sticky="nsew")
        self.__columns_listbox.grid(row=2, column=1, sticky="nsew")

        self.__apply_columns_style()
        self.__append_db_tables_listbox()

        root.mainloop()

    def _open_top_window(self,title,geometry):
        if not self._top_level_window:
            top = Toplevel(self._root_win)
            self._top_level_window = top
        else:
            self._refresh = True
            top = self._top_level_window
            top.update()
            top.update_idletasks()
        
        top.title(title)
        top.geometry(geometry)
    

    def __append_db_tables_listbox(self):
        if not self.__tables_listbox or not self.__columns_listbox:
            return False
        
        data = self._db_tables
        if len(data):
            window = self._root_win
            listbox = self.__tables_listbox

            for item in data:
                listbox.insert(END, item)

            date = self._get_date()
            def save_selection():
                self._selected_table = ""
                try:
                    selection = listbox.curselection()
                    self._selected_table = listbox.get(selection[0])
                    print(f"{date} - selected table: {self._selected_table}")
                    self.__append_columns_listbox()
                except (IndexError, AttributeError, TypeError, Exception) as e:
                    erh.SilentErrorHandler().log_error(f"{str(e)}")
                    print(f"{date} - Table not selected")
                
            save_button = Button(window, text="Select table", command=save_selection)
            save_button.grid(row=3, column=0,sticky="nsew")
        
        return True

    def __append_columns_listbox(self):
        if not self._conn:
            self._print_user_message("Not connected to database")
            return False
        
        query = f"SELECT * FROM information_schema.columns WHERE table_name = '{self._selected_table}'"
        erh.SilentErrorHandler().log_info(f"Columns select query: {query}")
        try:
            df = pd.read_sql(query, self._conn, columns="COLUMN_NAME")
            columns = df["COLUMN_NAME"].tolist()
            df = pd.read_sql(query, self._conn)
            print(df["COLUMN_NAME"] + " - " + df["DATA_TYPE"])

        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Could not get column names from database: {str(e)}")
            return False
       
        if len(columns):
            self._db_tab_columns = columns
            window = self._root_win

            self.__columns_listbox.delete(0, END)
            for column in columns:
                self.__columns_listbox.insert(END, column)

            save_button = Button(window, text="Select columns", command=self._save_columns)
            save_button.grid(row=3,column=1,sticky="nsew")
        
        return True

    def _save_columns(self):
        listbox = self.__columns_listbox
        self._selected_columns.clear()
        for i in listbox.curselection():
            self._selected_columns.append(listbox.get(i))
            if len(self._selected_columns):
                self._print_user_message(f"selected columns: {str(self._selected_columns)}")
            else:
                 print("Select columns first")


    def _create_folder(self,folder_path,message):
        if not len(folder_path):
            return False
        
        if not os.path.exists(folder_path):
            if len(message):
                self._print_user_message(message)
            try:
                os.mkdir(folder_path)
            except (Exception, AttributeError, TypeError) as e:
                erh.SilentErrorHandler.log_error(f"{str(e)}")
        
        return True
    
    def _sanitize_string(self,txt):
        txt = str(txt)
        txt = txt.replace("DROP"," ")
        txt = txt.replace("DELETE"," ")
        txt = txt.replace("UPDATE"," ")
        txt = txt.replace(";"," ")
        txt = txt.replace("`", " ")
        txt = txt.replace("\""," ")
        return txt
    
    def _get_date(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        return date
    
    def _print_user_message(self,msg):
        date = self._get_date()
        if not msg:
            print(f"{date}")
        print(f"{date} - {msg}")

    def __apply_columns_style(self):
        window = self._root_win
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)