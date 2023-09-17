import pandas as pd
import Database as db
import SilentErrorHandler as erh
import mod.Export as exporter
import mod.Import as importer

db_instance = db.Database()
connection = db_instance.connect()
db_instance.print_connection_info()
import mod.Import as importer

def main():
    importer.Import().open_import_window()

    # tables = get_db_tables()
    # exporter.Export(tables).open_window()

    importer.Import().open_import_window()

    
main()
