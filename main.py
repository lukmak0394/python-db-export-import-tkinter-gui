import pandas as pd
import Database as db
import SilentErrorHandler as erh
import mod.Export as exporter

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

    tables = get_db_tables()
    exporter.Export(tables).open_window()
    
main()






    