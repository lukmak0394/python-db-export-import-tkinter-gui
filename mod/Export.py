import os
from dotenv import load_dotenv
from tkinter import *
from tkinter import ttk
import pandas as pd
import sqlalchemy.exc as sqe
import SilentErrorHandler as erh
import mod.Module as core

class Export(core.Module):

    __export_folder = ""
    __export_formats = {
        1:"Excel",
        2:"CSV",
    }

    __query_conditions = []
    __conditions_start_row = 5
    __queries_to_add = {}

    __query_limit_input = None

    def __init__(self):
        super().__init__()
        load_dotenv()

    def open_window(self):
        super()._open_root_window("Export data from database", "Columns to be exported")
    
    def _save_columns(self,all=None):
        super()._save_columns(all)
        self.__display_export_buttons()
        self.__open_conditions_window()

    def __display_export_buttons(self):
        window = self._root_win
        export_formats = self.__export_formats
        i = 0
        for key in export_formats:
            btn_txt = f"Export {export_formats[key]}"
            export_format_btn = Button(window,text=btn_txt, command=lambda m=key: self.__export(m), bg="#0d6efd", fg="white")
            export_format_btn.grid(row=7,column=i, rowspan=2, sticky="nsew")
            i+=1

    def __open_conditions_window(self):
        super()._open_top_window("Set conditions", "550x250")
        top = self._top_level_window

        btn_add_row = Button(top, text="Add next", command=lambda m=top: self.__add_conditions_row(m), bg="#0d6efd", fg="white")
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

        if bool(self._refresh):
            self.__conditions_start_row = 5

        self.__add_conditions_row(top)

        top.mainloop()
    
    def __add_conditions_row(self,win):
        start_row = self.__conditions_start_row
        columns = self._db_tab_columns

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
            super()._print_user_message(f"export successfull - exported {rows} rows. File size: {os.path.getsize(file)} B")

            erh.SilentErrorHandler().log_info(f"Excel from {table_name} download")
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with file export: {str(e)}")
            super()._print_user_message("Unrecognized error")
            return False
        
    def __export_to_csv(self, subfolder_name, date, table_name, df):
        try:
            file = os.path.join(subfolder_name, f"{date}_{table_name}.csv")
            df.to_csv(file,index=True)
            rows = len(df)-1
            super()._print_user_message(f"export successfull - exported {rows} rows. File size: {os.path.getsize(file)} B")
            erh.SilentErrorHandler().log_info(f"CSV from {table_name} download")
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with file export: {str(e)}")
            super()._print_user_message("Unrecognized error")
            return False
        
    def __export(self,format):
        date = super()._get_date()

        if not format:
            super()._print_user_message("Invalid format. Export aborted")
            return False
        
        table_name = self._selected_table
        columns = self._selected_columns

        query = self.__prepare_export_query(columns,table_name)
        erh.SilentErrorHandler().log_info(f"Data select query: {query}")

        make_file = False
        try:
            df = pd.read_sql(f"{query}", self._conn)
            if(len(df) > 1):
                make_file = True
        except (sqe.ProgrammingError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error with getting data: {str(e)}")
            super()._print_user_message("Unrecognized error")
            return False
        
        if make_file:
            super()._create_folder(self.__export_folder,f"Export folder does not exist. Creating it now...")
            subfolder_name = os.path.join(self.__export_folder, table_name)
            super()._create_folder(subfolder_name,f"Creating subfolder '{table_name}...")

            if format == 1:
                self.__export_to_excel(subfolder_name,date,table_name,df)
            else:
                self.__export_to_csv(subfolder_name,date,table_name,df)
        else:
            super()._print_user_message("No data to export")

        return True


  