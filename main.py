import pandas as pd
import Database as db
import SilentErrorHandler as erh
import tkinter as tk
import Export as ex

db_instance = db.Database()
connection = db_instance.connect()

def main():
 
    def get_db_tables():
        try:
            df = pd.read_sql("SHOW TABLES", connection, columns=["Tables_in_world"])
            result = df["Tables_in_world"].tolist()
            return result
        except (TypeError, AttributeError) as e:
            erh.SilentErrorHandler().log_error(f"{str(e)}")
            return None

    def display_menu():
        print("****** SELECT AN ACTION TO PERFORM ******")
        print("Available actions:")
        print("1 - export \n")
        while True:
            act = input("Your choice: ")
            if act.isdigit():
                tables = get_db_tables()
                act = int(act)
                if act == 1:
                    ex.Export(tables).initialize()
                    break
            else:
                print("Must be a number")

    display_menu()
        
    


main()

        








    