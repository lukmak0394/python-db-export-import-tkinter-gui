# SilentErrorHandler

---

Class responsible for handling erros / warning especially in try catch blocks. It saves info to logs folder to file with logs for current day.

---

### Variables description

private **__log_format** - format for logging messages in log file. time, level (warning/info,err), message.

---

### Methods description

1. protected **__create_log_folder** - Creates logs folder.

2. protected **__get_log_filename** - prepares filename in which logs for current date will be put. 

3. protected **__log_error** - responsible for logging error messages. Uses traceback to log full information. 

4. proteced **__log_warning** - responsible for logging warning messages. Uses traceback to log full information.

5. protected **__log_info** - responsible for logging info messages. Do not use traceback. This is not required here - simply log user defined log message.

6. 
   
   
