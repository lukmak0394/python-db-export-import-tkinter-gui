import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class Database():

    _instance = None

    # enviornment: 1: production, 2: testing
    __enviornment = None

    # default connection parameters - to be used in test enviornment
    __conn_params = {
        "db_host":"localhost",
        "db_user":"root",
        "db_pwd":"",
        "db_name":"world"
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
        self.__define_environment()
        self.__set_conn_params()
        self.__set_conn_string()
        self.__create_engine()

    def __define_environment(self):
        while True:
            env = input("Define environment (1 - production; 2 - testing): ")
            if env.isdigit():
                env = int(env)
                if env == 1 or env == 2:
                    self.__enviornment = env
                    break
                else:
                    print("Please type 1 for production or 2 for testing")
            else:
                print("Must be a number")


    def __set_conn_params(self):
        self.__enviornment == None
        if not self.__enviornment:
            print("Environment not defined")
            self.__define_environment()
        
        if self.__enviornment == 1:
            self.__conn_params["db_host"] = input("Enter a database host (ex. localhost): ")
            self.__conn_params["db_user"] = input("Enter a database user (ex. root): ")
            self.__conn_params["db_pwd"] = input("Enter a database password (ex. admin): ")
            self.__conn_params["db_name"] = input("Enter a database name (ex. world): ")

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
            print("Connected to database: " + self.__conn_params["db_name"] + " as user: " + self.__conn_params["db_user"])
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
    


    
        

    
    

 
    