import os
import logging
import datetime
import traceback

# Write files to log file
class SilentErrorHandler:

    __logs_folder = ""
    
    __logs_file_name = ""

    # ERR (1 - default) / WARN (2)
    __log_type = None

    #log format for err ex 2023-09-10 20:39:38,239 - ERROR - TEST
    __log_format = '%(asctime)s - %(levelname)s - %(message)s'

    __traceback = None

    def __init__(self):
        self.__logs_folder = "logs"
        self.__create_log_folder()
        # Use traceback to pass full err info to log - paths, lines, script names 
        self.__traceback = traceback.format_exc()
        self.__logs_file_name = self.__get_log_filename()

    def __create_log_folder(self):
        if not os.path.exists(self.__logs_folder):
            os.mkdir(self.__logs_folder)

    def __get_log_filename(self):
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.__logs_folder, f"{today_date}.log")


    def log_error(self, error_message):
        logging.basicConfig(filename=self.__logs_file_name, level=logging.ERROR, format=self.__log_format)
        logging.error(f"{error_message}\n{self.__traceback}")

    def log_warning(self, warning_message):
        logging.basicConfig(filename=self.__logs_file_name, level=logging.WARNING, format=self.__log_format)
        logging.error(f"{warning_message}\n{self.__traceback}")

    



