# Python first project

---

### Description

I create it to have a desktop app that allows to connect to the database and export selected data to excel/csv.

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

- Export data from database 
  
  - It has simple GUI with tkinter
  - You can add conditions to your query like limit or where clause in separate window

- Import data to database (not started yet)

---

### Classes / modules

*Modules are put in /mod directory*

1. **main.py** - main script from which modules are called

2. **Database.py** - module that is responsible for making connection with a database. It takes connection parameters from .env file. 

3. **SilentErrorHandler.py** - this module is to handle exception errors. It creates a logs folder and log file in it and then puts message with error to the file. It uses traceback so it logs everything.

4. **Export.py**- export module. It is responsible for handling operations related to data export.: selecting columns to export, adding conditions, etc.

---



![](C:\Users\lmako\AppData\Roaming\marktext\images\2023-09-16-13-46-08-image.png)
