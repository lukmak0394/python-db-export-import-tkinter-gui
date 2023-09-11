import pandas as pd
import Database as db
import SilentErrorHandler as erh
import tkinter as tk

db_instance = db.Database()
connection = db_instance.connect()

def main():
 
    def get_db_tables():
        try:
            df = pd.read_sql("SHOW TABLES", connection, columns=["Tables_in_world"])
            result = df["Tables_in_world"].to_numpy()
            return result
        except (TypeError, AttributeError) as e:
            erh.SilentErrorHandler().log_error(f"{str(e)}")
            return None
    
    tables = get_db_tables()

    def create_columns_listbox(win, tables):
        if len(tables):
            columns = []
            for table in tables:
                df = pd.read_sql(f"SELECT COLUMN_NAME from information_schema.columns WHERE table_name = '{table}'", connection, columns="COLUMN_NAME")
                columns.extend(df["COLUMN_NAME"].to_numpy())

            if len(columns):

                columns_listbox = tk.Listbox(win, selectmode=tk.MULTIPLE)
                columns_listbox.pack(fill=tk.BOTH, expand=True)

                selected_columns = []

                for column in columns:
                    columns_listbox.insert(tk.END, column)
                    columns_listbox.pack(pady=10)

                def save_selection():
                    selected_columns.clear()
                    for i in columns_listbox.curselection():
                        selected_columns.append(columns_listbox.get(i))
                    print(selected_columns)

                save_button = tk.Button(win, text="Select columns", command=save_selection)
                save_button.pack()
        

    def create_db_tables_listbox():

        if len(tables):
            win = tk.Tk()
            win.title("My First Python Project")
            win.geometry("800x300")
            
            table_listbox = tk.Listbox(win, selectmode=tk.SINGLE)
            table_listbox.pack(fill=tk.BOTH, expand=True) 

            selected_tables = []

            for table in tables:
                table_listbox.insert(tk.END, table)
                table_listbox.pack(pady=10)

            def save_selection():
                selected_tables.clear()
                for i in table_listbox.curselection():
                    selected_tables.append(table_listbox.get(i))
                print(selected_tables)
                # create_columns_listbox(win, selected_tables)
        
            save_button = tk.Button(win, text="Select table", command=save_selection)
            save_button.pack()

            win.mainloop()
    
    def define_action():
        if not connection:
            return False
        
        while True:
            action = input("Please define desired action (1 - export [not active yet] / 2 - import [not active yet]):  ")
            if action.isdigit():
                action = int(action)
                if action == 1:
                    try:
                        create_db_tables_listbox()
                        break
                    except Exception:
                        erh.SilentErrorHandler().log_error(f"{str(e)}")
                else: 
                    print("Not allowed")
            else:
                print("Please enter a number.")

    define_action()

main()

        








    