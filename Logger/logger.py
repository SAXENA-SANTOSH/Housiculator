"""

 This is module for creating and maintaining System logs.
 
 Developed by Santosh Saxena 
 on 10/4/2021

"""


# Module declaration
#-----------------------------------------------------------#
import os 
import shutil
import datetime
#-----------------------------------------------------------#


class Logger:

    """
    This is logger class
    """
    def __init__(self , path):
        try:
            self.path = path
            file = open(path + "/Logger/Log_file.txt","w")
            file.write("\n")
            space = 18
            file.write("\n" + " "*space + "|¯¯¯|            |¯¯¯¯¯¯¯¯¯¯¯¯¯|  |¯¯¯¯¯¯¯¯¯¯¯¯¯|  |¯¯¯¯¯¯¯¯¯¯¯¯¯|")
            file.write("\n" + " "*space + "|   |            |             |  |             |  |             |")
            file.write("\n" + " "*space + "|   |            |   |¯¯¯¯¯|   |  |   |¯¯¯¯¯¯¯¯¯   |    |¯¯¯¯¯¯¯¯ ")
            file.write("\n" + " "*space + "|   |            |   |     |   |  |   |            |    |________ ")
            file.write("\n" + " "*space + "|   |            |   |     |   |  |   |   |¯¯¯¯¯|  |             |")
            file.write("\n" + " "*space + "|   |            |   |     |   |  |   |   |_    |  |_________    |")
            file.write("\n" + " "*space + "|   |            |   |     |   |  |   |     |   |            |   |")
            file.write("\n" + " "*space + "|   |_________   |   |_____|   |  |   |_____|   |   _________|   |")
            file.write("\n" + " "*space + "|             |  |             |  |             |  |             |")
            file.write("\n" + " "*space + "|_____________|  |_____________|  |_____________|  |_____________|")
            file.write("\n\n")
            file.write("=="*55 + "\n")
            file.write("  DATE     |   DAY   |     TIME     |   TYPE  |" + " "*27 + "MESSAGE\n")
            file.write("=="*55)
            file.write("\n")
            file.close()
        except Exception as e:
            pass

    def generate_metadata_logs(self):

        """
        This is a function which will generate meta data for logs
        """

        try:
            #if(os.path.isfile(self.path + "/Logger/Log_file_metadata.txt")):
            #    shutil.rmtree(self.path + "/Logger/Log_file_metadata.txt")
            file = open(self.path + "/Logger/Log_file_metadata.txt","w")
            file.write("\n")
            file.write("=="*55)
            file.write("\n\nLogs Metadata\n")
            file.write("--"*55)
            file.write("\nAll the activities done by code is recorded in log files")
            file.write("\n\nMessage : Message will give status of the execution process.")
            file.write("\n\nTypes : There are 9 types of log message\n")
            file.write("--"*55)
            file.write("\n\n")
            file.write("1) BEG : This indicates that your pipeline has been intialized by the system.\n")
            file.write("2) END : This indicates that your pipeline has been executed by the system.\n")
            file.write("3) CHK : This indicates that your function has been initialized by the system.\n")
            file.write("4) PAS : This indicates that your function has been successfully executed by the system.\n")
            file.write("5) ERR : This indicates in which section and function you code is failed.\n")
            file.write("6) LIN : This indicates in which line your code has failed.\n")
            file.write("7) TYP : This indicates what is type of error your system has received\n")
            file.write("8) INF : This indicates any general information selected by the code at runtime\n")
            file.write("9) NAM : This indicates the name of the module which will work as a kind of heading")
            file.write("\n\n")
            file.write("=="*55)
            file.close()
        except :
            pass

    def add_in_logs(self,type_ , message):

        """
        This function will append the log messages into log file.

        There are 3 types of logs

        1) Begin --> BEG
        2) End   --> END
        3) Check --> CHK
        4) Pass  --> PAS
        5) Error --> ERR
        6) Line no > LIN
        7) Type  --> TYP
        8) information ----> INF
        9) name  --> NAM --> for title and for developers 
        
        """


        try:
            self.message = message.upper()
            self.type = type_.upper()
            file = open(self.path+"/Logger/Log_file.txt","a")
            date = datetime.datetime.now().strftime("%D")
            day = datetime.datetime.now().strftime("%a").upper()
            time = datetime.datetime.now().strftime("%H:%M:%S")

            if(self.type == "BEG"):
                file.write("--"*55+"\n" )
                file.write(str(date)+"   |   "+str(day)+"   |   "+str(time)+"   |   "+str(self.type) +"   |   "+ str(self.message)+"\n")
                file.write("--"*55)
                file.write("\n")
                file.close()
            elif(self.type == "END"):
                file.write(str(date)+"   |   "+str(day)+"   |   "+str(time)+"   |   "+str(self.type) +"   |   "+ str(self.message)+"\n")
                file.write("--"*55 + "\n")
                file.close()
            elif(self.type == "NAM"):
                file.write("\n")
                file.write(" "*45 + self.message + "\n")
                file.close()
            else:
                file.write(str(date)+"   |   "+str(day)+"   |   "+str(time)+"   |   "+str(self.type) +"   |   "+ str(self.message)+"\n")
                file.close()
        except :
            pass