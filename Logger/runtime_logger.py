"""

 This is module for creating and maintaining System logs.
 
 Developed by Santosh Saxena 
 on 10/4/2021

"""


# Module declaration
#-----------------------------------------------------------#
import datetime
#-----------------------------------------------------------#


class Runtime_Logger:

    """
    This is logger class
    """
    def __init__(self , path):
        try:
            self.path = path
            file = open(path + "/Logger/runtime_Log_file.txt","w")
            file.write("\n\n")
            file.write("=="*55 + "\n")
            file.write("  DATE         DAY         TIME       " + " "*27 + "MESSAGE\n")
            file.write("=="*55)
            file.write("\n")
            file.close()
        except Exception as e:
            pass

    def add_in_logs(self, message):

        try:
            self.message = message.upper()
            file = open(self.path+"/Logger/runtime_Log_file.txt","a")
            date = datetime.datetime.now().strftime("%D")
            day = datetime.datetime.now().strftime("%a").upper()
            time = datetime.datetime.now().strftime("%H:%M:%S")
        
            file.write(str(date)+"       "+str(day)+"       "+str(time)+"       "+ str(self.message)+"\n")
            file.close()
        except :
            pass