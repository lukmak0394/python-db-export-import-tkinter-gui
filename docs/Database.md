# Database

---

This is singleton class responsible for handling database connection process.

---

### Methods description

1. protected **__initialize** - Responsible for calling methods setting connection parameters. Called in __new__ when class instance created.

2. protected **__define_environment** - set enviornment - testing / prod. defined in .env. Dependint on this other db conn params will be set.

3. protected **__set_conn_params** - set connection parameters - defined in .env - host, user, pwd, dbname.

4. protected **__set_conn_string** - create connection string to make a connection.

5. proteced **__create_engine** - creates db connection engine using prepared connection string.

6. protected **__print_connection_info** - prints connection info. status, current enviornment, database and user.

7. public **connect** - connect to database. 

8. public **disconnect** - disconnect from database.
