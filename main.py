import pandas as pd
import Database as db
import SilentErrorHandler as erh
import tkinter as tk
import mod.Export as ex

connection = db.Database().connect()
db.Database().print_connection_info()

def main():
 
    def get_db_tables():
        try:
            df = pd.read_sql("SHOW TABLES", connection, columns=["Tables_in_world"])
            result = df["Tables_in_world"].tolist()
            return result
        except (TypeError, AttributeError) as e:
            erh.SilentErrorHandler().log_error(f"{str(e)}")
            return None

    tables = get_db_tables()
    ex.Export(tables).open_window()
    db.Database().disconnect()
    
main()






    