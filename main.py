import pandas as pd
import Database as db
import SilentErrorHandler as erh
import mod.Export as exporter
import mod.Import as importer

db_instance = db.Database()
connection = db_instance.connect()
db_instance.print_connection_info()

def main():

    tables = db_instance.get_tables(connection)
    exporter.Export(tables).open_window()
    # importer.Import().open_import_window()

    
main()
