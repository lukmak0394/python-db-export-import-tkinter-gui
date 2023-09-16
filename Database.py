import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import SilentErrorHandler as erh

class Database():

    _instance = None

    __enviornment = None

    __conn_params = {
        "db_host":None,
        "db_user":None,
        "db_pwd":None,
        "db_name":None
    }

    __connection_string = ""

    __engine = None

    __status = False

    # Only one instance allowed - signleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.__initialize()
        return cls._instance
    
    def __initialize(self):
        load_dotenv()
        try:
            self.__define_environment()
            self.__set_conn_params()
            self.__set_conn_string()
            self.__create_engine()
        except (TypeError, AttributeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"{str(e)}")
            return False
      

    def __define_environment(self):
        env = os.getenv("enviornment")
        if bool(env):
            if env.isdigit():
                env = int(env)
                if env == 1 or env == 2:
                    self.__enviornment = env
            else:
                print("Assigned value must be a number")

        else:
            print("Enviornment not defined in .env file")


    def __set_conn_params(self):
        type_name = "test"
        if self.__enviornment == 1:
            type_name = "prod"

        self.__conn_params["db_host"] = os.getenv(f"db_host.{type_name}")
        self.__conn_params["db_user"] = os.getenv(f"db_user.{type_name}")
        self.__conn_params["db_pwd"] = os.getenv(f"db_pass.{type_name}")
        self.__conn_params["db_name"] = os.getenv(f"db_name.{type_name}")
           
    def __set_conn_string(self):
        host = self.__conn_params["db_host"]
        user = self.__conn_params["db_user"]
        pwd = self.__conn_params["db_pwd"] 
        name = self.__conn_params["db_name"]
        self.__connection_string = "mysql+mysqlconnector://" + user + ":"+ pwd + "@" + host + "/" + name

    def __create_engine(self):
        self.__engine = create_engine(self.__connection_string)

    
    def print_connection_info(self):
        db_name = self.__conn_params["db_name"]
        db_user = self.__conn_params["db_user"]
        status_name = "NOT CONNECTED"
        if self.__enviornment == 1:
            env_name = "production"
        else:
            env_name = "testing"
        if self.__status:
            status_name = "CONNECTED"
        print(f"STATUS: {status_name} || ENVIORNMENT: {env_name} || DATABASE: {db_name} || USER: {db_user}")

    def get_engine(self):
        return self.__engine
    
    def connect(self):
        try:
            connection = self.__engine.connect()
            self.__status = True
            return connection
        except (SQLAlchemyError, AttributeError, TypeError, Exception) as e:
            erh.SilentErrorHandler().log_error(f"Error connecting to the database: {str(e)}")
            return None
        
    def disconnect(self):
        if not self.conn:
            return None
        
        self.conn.close()

        

