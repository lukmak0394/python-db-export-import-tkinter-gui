import Database as db
import SilentErrorHandler as erh
import tkinter as tk
from tkinter import ttk
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
import sqlalchemy.exc as sqe

class Export:

    __conn = None

    __tk_window = None
    __tk_window_title = ""

    __columns_listbox = None
    __tables_listbox = None

    __db_tables = None

    __selected_table = ""
    __selected_columns = []

    __export_folder = ""

    __export_formats = {
        1:"Excel",
        2:"CSV",
    }

    __condition_rows_counter = 2

    def __init__(self,tables,connection):
        if not connection:
            return None
        
        if not isinstance(tables, list):
            return None
        
        load_dotenv()
        self.__conn = connection
        self.__tk_window_title = "Export data from database"
        self.__tk_window = tk.Tk()
        self.__db_tables = tables
        self.__export_folder = os.getenv("export_folder")


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
            return False
        
        data = self.__db_tables
        if len(data):
            window = self.__tk_window
            listbox = self.__tables_listbox

            for item in data:
                listbox.insert(tk.END, item)

            def save_selection():
                self.__selected_table = ""
                selection = listbox.curselection()
                self.__selected_table = listbox.get(selection[0])
                date = self.__get_date()
                print(f"{date} - selected table: {self.__selected_table}")
                self.__insert_column_names_to_listbox()
                
            save_button = tk.Button(window, text="Save table", command=save_selection)
            save_button.grid(row=2, column=0,sticky="nsew")
        
        return True
    

    def __insert_column_names_to_listbox(self):
        date = self.__get_date()

        if not self.__conn:
            print(f"{date} - Not connected to database")
            return False
        
        query = f"SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = '{self.__selected_table}'"
        print(f"{date} - query: {query}")

        try:
            df = pd.read_sql(query, self.__conn, columns="COLUMN_NAME")
            columns = df["COLUMN_NAME"].tolist()
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Could not get column names from database: {str(e)}")
            return False
       
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
                print(f"{date} - selected columns: {str(self.__selected_columns)}")
                self.__display_export_buttons()
                self.__open_conditions_window(columns)

            save_button = tk.Button(window, text="Select columns", command=save_selection)
            save_button.grid(row=2,column=1,sticky="nsew")
        
        return True

    def __display_export_buttons(self):
        window = self.__tk_window
        export_formats = self.__export_formats
        i = 0
        for key in export_formats:
            btn_txt = f"Export {export_formats[key]}"
            export_format_btn = tk.Button(window,text=btn_txt, command=lambda m=key: self.__export(m), bg="#0d6efd", fg="white")
            export_format_btn.grid(row=3,column=i, sticky="nsew")
            i+=1

    def __open_conditions_window(self,cols):

        window = tk.Tk()

        window.title("Set conditions")
        window.geometry("600x200")

        btn_add_row = tk.Button(window, text="Add condition row", command=lambda m=window, c=cols: self.__add_conditions_row(window,cols))
        btn_add_row.grid(row=1, column=1, columnspan=5)

        # submit_button = tk.Button(window, text="Submit", command=lambda s=stmts_select,c=cols_select,cd=condition_select,cv=cond_val_input,l=limit_input: self.__submit_query_conditions(s,c,cd,cv,l))
        # submit_button.grid(row=2, column=1, columnspan=5)

        window.mainloop()
    
    def __add_conditions_row(self,win,columns):

        rows_counter = self.__condition_rows_counter

        if(rows_counter == 2):
            conditional_expressions = ["WHERE", "AND", "OR"]
        else:
            conditional_expressions = ["AND", "OR"]
        
        selected_expr = tk.StringVar()
        expr_select = ttk.Combobox(win, textvariable=selected_expr, values=conditional_expressions)
        expr_select.grid(row=rows_counter,column=1,sticky="nsew")

        selected_col = tk.StringVar()
        columns_select = ttk.Combobox(win,textvariable=selected_col,values=columns)
        columns_select.grid(row=rows_counter,column=2,sticky="nsew")

        operators = ["=", ">", "<", ">=", "<=", "LIKE","NOT LIKE"]
        selected_operator = tk.StringVar()
        operators_select = ttk.Combobox(win, textvariable=selected_operator, values=operators)
        operators_select.grid(row=rows_counter,column=3,sticky="nsew")
        
        condition_val_input = tk.Entry(win)
        condition_val_input.grid(row=rows_counter,column=4,sticky="nsew")

        limit_input = tk.Entry(win)
        limit_input.grid(row=rows_counter,column=5,sticky="nsew")

        self.__condition_rows_counter += 1



    # def __submit_query_conditions(self,stmt,col,cond,val,limit):
    #     selected_condition_stmt = stmt.get()
    #     selected_column = col.get()
    #     selected_cond = cond.get()
    #     condition_val = val.get()
    #     query_limit = limit.get()

    #     query_condition = f"{selected_condition_stmt} {selected_column} {selected_cond} {selected_cond} LIMIT {query_limit}"

    #     condition_query = {"condition": query_condition}
    #     print(condition_query)
            

    def __prepare_export_query(self, columns, table):
        query = "SELECT "
        for column in columns:
            query += column + ", " 
        query = query.rstrip(", ")
        query += f" FROM {table}"
        return query
    
    def __export_to_excel(self, subfolder_name, date, table_name, df):
        try:
            file = os.path.join(subfolder_name, f"{date}_{table_name}.xlsx")
            df.to_excel(file,index=True)
            print(f"{date} - export successfull")
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with file export: {str(e)}")
            print(f"{date} - Error occoured")
            return False
        
    def __export_to_csv(self, subfolder_name, date, table_name, df):
        try:
            file = os.path.join(subfolder_name, f"{date}_{table_name}.csv")
            df.to_csv(file,index=True)
            print(f"{date} - export successfull")
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with file export: {str(e)}")
            print(f"{date} - Error occoured")
            return False
    
    def __export(self,format):
        date = self.__get_date()

        if not format:
            print(f"{date} - Invalid format. Export aborted.")
            return False
        
        if not os.path.exists(self.__export_folder):
            print(f"{date} - Export folder does not exist. Creating it now...")
            os.mkdir(self.__export_folder)

        table_name = self.__selected_table
        columns = self.__selected_columns

        subfolder_name = os.path.join(self.__export_folder, table_name)
        if not os.path.exists(subfolder_name):
            print(f"{date} - Creating subfolder '{table_name}'...")
            os.mkdir(subfolder_name)
    
        query = self.__prepare_export_query(columns,table_name)
        try:
            df = pd.read_sql(f"{query}", self.__conn)
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with getting data: {str(e)}")
            print(f"{date} - Error occoured")
            return False
        
        if format == 1:
            self.__export_to_excel(subfolder_name,date,table_name,df)
        else:
            self.__export_to_csv(subfolder_name,date,table_name,df)

        return True


    def __get_date(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        return date

    def __apply_columns_style(self):
        window = self.__tk_window
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)


 

        
