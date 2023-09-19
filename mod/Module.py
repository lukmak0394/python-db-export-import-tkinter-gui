import os
import datetime
import SilentErrorHandler as erh

class Module():

    def _create_folder(self,folder_path,message):
        if not len(folder_path):
            return False
        
        if not os.path.exists(folder_path):
            if len(message):
                print(message)
            try:
                os.mkdir(folder_path)
            except (Exception, AttributeError, TypeError) as e:
                erh.SilentErrorHandler.log_error(f"{str(e)}")
        
        return True
    
    def _sanitize_string(self,txt):
        txt = str(txt)
        txt = txt.replace("DROP"," ")
        txt = txt.replace("DELETE"," ")
        txt = txt.replace("UPDATE"," ")
        txt = txt.replace(";"," ")
        txt = txt.replace("`", " ")
        txt = txt.replace("\""," ")
        return txt
    
    def _get_date(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        return date
    
    def _print_user_message(self,msg):
        date = self._get_date()
        if not msg:
            print(f"{date}")
        print(f"{date} - {msg}")