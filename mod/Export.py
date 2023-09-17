import os
from dotenv import load_dotenv
from tkinter import *
from tkinter import ttk
import pandas as pd
import datetime
import sqlalchemy.exc as sqe
import Database as db
import SilentErrorHandler as erh
import mod.Module as core

class Export(core.Module):

    __conn = None

    __tk_root_window = None
    __tk_root_window_title = ""
    __top_level_window = None

    __columns_listbox = None
    __tables_listbox = None

    __db_tables = []

    __selected_table = ""
    __selected_columns = []

    __export_folder = ""

    __export_formats = {
        1:"Excel",
        2:"CSV",
    }

    __query_conditions = []
    __conditions_start_row = 5
    __queries_to_add = {}

    __query_limit_input = None

    # Assign most necessary data - folder, tables, create root window
    def __init__(self,tables):
        
        if not isinstance(tables, list):
            return None
        
        load_dotenv()
        connection =  db.Database().connect()
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

        label_tables = Label(win, text="Database tables")
        label_tables.grid(row=1, column=0, sticky="nsew")
        label_columns = Label(win, text="Columns to select")
        label_columns.grid(row=1, column=1, sticky="nsew")

        self.__tables_listbox = Listbox(win, selectmode=SINGLE)
        self.__columns_listbox = Listbox(win, selectmode=MULTIPLE)
        self.__tables_listbox.grid(row=2, column=0, sticky="nsew")
        self.__columns_listbox.grid(row=2, column=1, sticky="nsew")

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

            date = super()._get_date()
            def save_selection():
                self.__selected_table = ""
                try:
                    selection = listbox.curselection()
                    self.__selected_table = listbox.get(selection[0])
                    print(f"{date} - selected table: {self.__selected_table}")
                    self.__insert_column_names_to_listbox()
                except (IndexError, AttributeError, TypeError, Exception) as e:
                    erh.SilentErrorHandler().log_error(f"{str(e)}")
                    print(f"{date} - Table not selected")
                
            save_button = Button(window, text="Select table", command=save_selection)
            save_button.grid(row=3, column=0,sticky="nsew")
        
        return True
    

    def __insert_column_names_to_listbox(self):
        date = super()._get_date()

        if not self.__conn:
            print(f"{date} - Not connected to database")
            return False
        
        query = f"SELECT * FROM information_schema.columns WHERE table_name = '{self.__selected_table}'"
        erh.SilentErrorHandler().log_info(f"Columns select query: {query}")
        try:
            df = pd.read_sql(query, self.__conn, columns="COLUMN_NAME")
            columns = df["COLUMN_NAME"].tolist()
            df = pd.read_sql(query, self.__conn)
            print(df["COLUMN_NAME"] + " - " + df["DATA_TYPE"])
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
                if len(self.__selected_columns):
                    print(f"{date} - selected columns: {str(self.__selected_columns)}")
                    self.__display_export_buttons()
                    self.__open_conditions_window(columns)
                else:
                    print("Select columns first")

            save_button = Button(window, text="Select columns", command=save_selection)
            save_button.grid(row=3,column=1,sticky="nsew")
        
        return True

    def __display_export_buttons(self):
        window = self.__tk_root_window
        export_formats = self.__export_formats
        i = 0
        for key in export_formats:
            btn_txt = f"Export {export_formats[key]}"
            export_format_btn = Button(window,text=btn_txt, command=lambda m=key: self.__export(m), bg="#0d6efd", fg="white")
            export_format_btn.grid(row=7,column=i, rowspan=2, sticky="nsew")
            i+=1

    def __open_conditions_window(self,cols):
        refresh = False

        if not self.__top_level_window:
            top = Toplevel(self.__tk_root_window)
            self.__top_level_window = top
        else:
            refresh = True
            top = self.__top_level_window
            top.update()
            top.update_idletasks()

        top.title("Set conditions")
        top.geometry("550x250")

        btn_add_row = Button(top, text="Add next", command=lambda m=top, c=cols: self.__add_conditions_row(m,c), bg="#0d6efd", fg="white")
        btn_add_row.grid(row=1, column=1, columnspan=4, sticky="nsew")
        submit_button = Button(top, text="Submit", command=self.__submit_query_conditions)
        submit_button.grid(row=2, column=1, columnspan=4, sticky="nsew")

        if self.__conditions_start_row == 5:
            limit_label = Label(top, text="Limit results")
            limit_label.grid(row=3, column=1, sticky="nsew")
            query_limit = StringVar()
            query_limit_input = Entry(top,textvariable=query_limit)
            query_limit_input.grid(row=3,column=2, columnspan=3, sticky="nsew")

            self.__query_limit_input = query_limit_input
            label_expr = Label(top, text="Expression")
            label_expr.grid(row=4, column=1, sticky="nsew")

            label_col = Label(top, text="Column")
            label_col.grid(row=4, column=2, sticky="nsew")

            label_operator = Label(top, text="Operator")
            label_operator.grid(row=4, column=3, sticky="nsew")

            label_value = Label(top, text="Value")
            label_value.grid(row=4, column=4, sticky="nsew")


        if bool(refresh):
            self.__conditions_start_row = 5

        self.__add_conditions_row(top,cols)

        top.mainloop()
    
    def __add_conditions_row(self,win,columns):
        start_row = self.__conditions_start_row

        if(start_row == 5):
            conditional_expressions = ["WHERE"]
        else:
            conditional_expressions = ["AND", "OR"]
        
        selected_expression  = StringVar()
        expr_select = ttk.Combobox(win, textvariable=selected_expression, values=conditional_expressions, state="readonly")
        expr_select.grid(row=start_row,column=1,sticky="nsew")

        selected_col = StringVar()
        column_select = ttk.Combobox(win,textvariable=selected_col,values=columns, state="readonly")
        column_select.grid(row=start_row,column=2,sticky="nsew")

        operators = ["=", "<>", ">", "<", ">=", "<=", "LIKE %", "% LIKE", "%LIKE%"]
        selected_operator = StringVar()
        operators_select = ttk.Combobox(win, textvariable=selected_operator, values=operators, state="readonly")
        operators_select.grid(row=start_row,column=3,sticky="nsew")

        condition_val = StringVar()
        condition_val_input = Entry(win, textvariable=condition_val)
        condition_val_input.grid(row=start_row,column=4,sticky="nsew")

        self.__query_conditions.append({
            'selected_expr': selected_expression,
            'selected_col': selected_col,
            'selected_operator': selected_operator,
            'condition_val_input': condition_val_input
        })
               
        self.__conditions_start_row += 1

    def __submit_query_conditions(self):
        self.__queries_to_add = {}
        i = 0
        for conditions in self.__query_conditions:
            expr = conditions['selected_expr'].get()
            col = conditions['selected_col'].get()
            operator = conditions['selected_operator'].get()
            val = super()._sanitize_string(conditions['condition_val_input'].get())

            if operator == "LIKE %":
                val = f"'{val}%'"
            elif operator == "% LIKE":
                val = f"'%{val}'"
            elif operator == "%LIKE%":
                val = f"'%{val}%'"
            else:
                val = f"'{val}'"

            if operator.find("%") != -1:
                operator = "LIKE"

            if len(expr) > 0 and len(col) > 0 and len(operator) > 0:
                self.__set_queries_to_add(expr,col,operator,val,i)

            i += 1
    
    def __set_queries_to_add(self,expr,col,oper,val,i):
        query = f" {expr} {col} {oper} {val} "
        self.__queries_to_add[i] = query


    def __prepare_export_query(self, columns, table):
        query = "SELECT "
        for column in columns:
            query += column + ", " 
        query = query.rstrip(", ")
        query += f" FROM {table}"

        queries_to_add = self.__queries_to_add.items()
        if len(queries_to_add):
            for key, value in queries_to_add:
                query += value

        limit = self.__query_limit_input.get()
        limit = super()._sanitize_string(limit)
        
        if len(limit) > 0:
            query += f" LIMIT {limit}"
        
        return query
    
    def __export_to_excel(self, subfolder_name, date, table_name, df):
        try:
            file = os.path.join(subfolder_name, f"{date}_{table_name}.xlsx")
            df.to_excel(file,index=True)
            rows = len(df)-1
            print(f"{date} - export successfull - exported {rows} rows. File size: {os.path.getsize(file)} B)")
            erh.SilentErrorHandler().log_info(f"Excel from {table_name} download")
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with file export: {str(e)}")
            print(f"{date} - Unrecognized error")
            return False
        
    def __export_to_csv(self, subfolder_name, date, table_name, df):
        try:
            file = os.path.join(subfolder_name, f"{date}_{table_name}.csv")
            df.to_csv(file,index=True)
            rows = len(df)-1
            print(f"{date} - export successfull - exported {rows} rows. File size: {os.path.getsize(file)} B)")
            erh.SilentErrorHandler().log_info(f"CSV from {table_name} download")
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with file export: {str(e)}")
            print(f"{date} - Unrecognized error")
            return False
        
    def __export(self,format):
        date = super()._get_date()

        if not format:
            print(f"{date} - Invalid format. Export aborted.")
            return False
        
        table_name = self.__selected_table
        columns = self.__selected_columns

        query = self.__prepare_export_query(columns,table_name)
        erh.SilentErrorHandler().log_info(f"Data select query: {query}")

        make_file = False
        try:
            df = pd.read_sql(f"{query}", self.__conn)
            if(len(df) > 1):
                make_file = True
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with getting data: {str(e)}")
            print(f"{date} - Unrecognized error")
            return False
        
        if make_file:
            super()._create_folder(self.__export_folder,f"{date} - Export folder does not exist. Creating it now...")
            subfolder_name = os.path.join(self.__export_folder, table_name)
            super()._create_folder(subfolder_name,f"{date} - Creating subfolder '{table_name}...")

            if format == 1:
                self.__export_to_excel(subfolder_name,date,table_name,df)
            else:
                self.__export_to_csv(subfolder_name,date,table_name,df)
        else:
            print(f"{date} - No data to export")

        return True

    def __apply_columns_style(self):
        window = self.__tk_root_window
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)

  