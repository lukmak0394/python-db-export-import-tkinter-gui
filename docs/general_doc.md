# Python first project

---

### Description

I create it to have a desktop app that allows me to export / import data from / to database in Excel / CSV. 

---

### Requirements

- pandas installed
  
  - install with pip using *pip install pandas*

- sqlalchemy installed
  
  - install with pip using pip install *pip install SQLAlchemy*

- dotenv installed
  
  - install with pip using *pip install dotenv*

- tkinter installed
  
  - instal with pip using *pip install tk*

---

### Functionalities

- Export data from database (in progress)
  
  - It has simple GUI with tkinter

- Import data to database (not started yet)

---

### Classes / modules

1. **main.py** - main script from which modules will be called

2. **Database.py** - module that is responsible for making connection with a database. It takes connection parameters from .env file 

3. **SilentErrorHandler.py** - this module is to handle exception errors. It creates a logs folder and log file in it and then puts message with error to the file. It uses traceback so it logs everything.

4. **Export.py**- export module. It is responsible for handling operations related to data export.: selecting columns to export, adding conditions, etc.

---

### 
