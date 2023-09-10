import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class Database():

    _instance = None

    # enviornment: 1: production, 2: testing
    __enviornment = None

    # default connection parameters - to be used in test enviornment
    __conn_params = {
        "db_host":None,
        "db_user":None,
        "db_pwd":None,
        "db_name":None
    }

    __connection_string = ""

    __engine = None

    # Create only one instance of my Database class - singleton 
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        load_dotenv()
        self.__define_environment()
        if self.__enviornment:
            self.__set_conn_params()
            self.__set_conn_string()
            self.__create_engine()

    def __define_environment(self):
        env = os.getenv("enviornment")
        if bool(env):
            if env.isdigit():
                env = int(env)
                if env == 1 or env == 2:
                    self.__enviornment = env
            else:
                print("Defined enviornment must be a number")
        else:
            print("Enviornment not defined in .env file")


    def __set_conn_params(self):
        self.__enviornment == None
        if not self.__enviornment or self.__enviornment:
            print("Environment not defined")
            self.__define_environment()
        
        if self.__enviornment == 1:
            self.__conn_params["db_host"] = input("Enter a database host (ex. localhost): ")
            self.__conn_params["db_user"] = input("Enter a database user (ex. root): ")
            self.__conn_params["db_pwd"] = input("Enter a database password (ex. admin): ")
            self.__conn_params["db_name"] = input("Enter a database name (ex. world): ")
        else:
            self.__conn_params["db_host"] = os.getenv("db_host")
            self.__conn_params["db_user"] = os.getenv("db_user")
            self.__conn_params["db_pwd"] = os.getenv("db_pass")
            self.__conn_params["db_name"] = os.getenv("db_name")

    def __get_conn_params(self):
        return self.__conn_params
    
    def __set_conn_string(self):
        host = self.__conn_params["db_host"]
        user = self.__conn_params["db_user"]
        pwd = self.__conn_params["db_pwd"] 
        name = self.__conn_params["db_name"]
        self.__connection_string = "mysql+mysqlconnector://" + user + ":"+ pwd + "@" + host + "/" + name
    
    def __create_engine(self):
        self.__engine = create_engine(self.__connection_string)

    def get_engine(self):
        return self.__engine
    
    def connect(self):
        try:
            connection = self.__engine.connect()
            if self.__enviornment == 1:
                env_name = "production"
            else:
                env_name = "testing"
            dbname = self.__conn_params["db_name"]
            dbuser = self.__conn_params["db_user"]
            print(f"STATUS: CONNECTED || ENVIORNMENT: {env_name} || DATABASE: {dbname} || USER: {dbuser}")
            return connection
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {str(e)}")
            return None
        
    def get_db_tables(self):
        connection = self.connect()
        if connection:
            df = pd.read_sql("SHOW TABLES", connection)
            connection.close()
            return df

    def display_conn_params(self):
        print("Database Connection Parameters:")
        conn_params = self.__get_conn_params()
        for key, value in conn_params.items():
            print(f"{key}: {value}")
    


    
        

    
    

 
    