import os
from dotenv import load_dotenv
import Database as db
import SilentErrorHandler as erh
from tkinter import *
from tkinter import ttk
import pandas as pd
import datetime
import sqlalchemy.exc as sqe

class Export:

    __conn = None

    __tk_root_window = None
    __tk_root_window_title = ""

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

    __condition_rows_counter = 3
    __query_conditions = []

    def __init__(self,tables,connection):
        if not connection:
            return None
        
        if not isinstance(tables, list):
            return None
        
        load_dotenv()
        self.__conn = connection
        self.__tk_root_window_title = "Export data from database"
        self.__tk_root_window = Tk()
        self.__db_tables = tables
        self.__export_folder = os.getenv("export_folder")


    def open_window(self):
        if not self.__tk_root_window or not self.__conn:
            return False
        
        win = self.__tk_root_window
        win.title(self.__tk_root_window_title)
        win.geometry("800x300")

        self.__tables_listbox = Listbox(win, selectmode=SINGLE)
        self.__columns_listbox = Listbox(win, selectmode=MULTIPLE)
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
            window = self.__tk_root_window
            listbox = self.__tables_listbox

            for item in data:
                listbox.insert(END, item)

            def save_selection():
                self.__selected_table = ""
                selection = listbox.curselection()
                self.__selected_table = listbox.get(selection[0])
                date = self.__get_date()
                print(f"{date} - selected table: {self.__selected_table}")
                self.__insert_column_names_to_listbox()
                
            save_button = Button(window, text="Save table", command=save_selection)
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
            window = self.__tk_root_window
            listbox = self.__columns_listbox

            listbox.delete(0, END)
            for column in columns:
                listbox.insert(END, column)

            def save_selection():
                self.__selected_columns.clear()
                for i in listbox.curselection():
                    self.__selected_columns.append(listbox.get(i))
                print(f"{date} - selected columns: {str(self.__selected_columns)}")
                self.__display_export_buttons()
                self.__open_conditions_window(columns)

            save_button = Button(window, text="Select columns", command=save_selection)
            save_button.grid(row=2,column=1,sticky="nsew")
        
        return True

    def __display_export_buttons(self):
        window = self.__tk_root_window
        export_formats = self.__export_formats
        i = 0
        for key in export_formats:
            btn_txt = f"Export {export_formats[key]}"
            export_format_btn = Button(window,text=btn_txt, command=lambda m=key: self.__export(m), bg="#0d6efd", fg="white")
            export_format_btn.grid(row=3,column=i, sticky="nsew")
            i+=1

    def __open_conditions_window(self,cols):
        top = Toplevel()
        top.title("Set conditions")
        top.geometry("500x200")

        btn_add_row = Button(top, text="Add next", command=lambda m=top, c=cols: self.__add_conditions_row(m,c), bg="#0d6efd", fg="white")
        btn_add_row.grid(row=1, column=1, columnspan=4, sticky="nsew")

        submit_button = Button(top, text="Submit", command=self.submit_values)
        submit_button.grid(row=2, column=1, columnspan=4, sticky="nsew")

        self.__add_conditions_row(top,cols)

        top.mainloop()
    
    def __add_conditions_row(self,win,columns):
        rows_counter = self.__condition_rows_counter

        if(rows_counter == 3):
            conditional_expressions = ["WHERE", "AND", "OR"]
        else:
            conditional_expressions = ["AND", "OR"]
        
        selected_expression  = StringVar()
        expr_select = ttk.Combobox(win, textvariable=selected_expression, values=conditional_expressions)
        expr_select.grid(row=rows_counter,column=1,sticky="nsew")

        selected_col = StringVar()
        column_select = ttk.Combobox(win,textvariable=selected_col,values=columns)
        column_select.grid(row=rows_counter,column=2,sticky="nsew")

        operators = ["=", ">", "<", ">=", "<=", "LIKE","NOT LIKE"]
        selected_operator = StringVar()
        operators_select = ttk.Combobox(win, textvariable=selected_operator, values=operators)
        operators_select.grid(row=rows_counter,column=3,sticky="nsew")

        condition_val_input = Entry(win)
        condition_val_input.grid(row=rows_counter,column=4,sticky="nsew")

        self.__query_conditions.append({
            'selected_expr': selected_expression,
            'selected_col': selected_col,
            'selected_operator': selected_operator,
            'condition_val_input': condition_val_input
        })
               
        self.__condition_rows_counter += 1

    def submit_values(self):
        for conditions in self.__query_conditions:

            expr = conditions['selected_expr'].get()
            col = conditions['selected_col'].get()
            oper = conditions['selected_operator'].get()
            val = conditions['condition_val_input'].get()

            if len(expr) and len(col) and len(oper) and len(val):
                row_data = {
                    "expression": conditions['selected_expr'].get(),
                    "column": conditions['selected_col'].get(),
                    "operator": conditions['selected_operator'].get(),
                    "value": conditions['condition_val_input'].get()
                }
                print(row_data)


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
        window = self.__tk_root_window
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)


 

        
