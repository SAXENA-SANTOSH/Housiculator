"""
This class will validate file name of the dataset and classify the good files in good folder and bad files in bad folder

Developed by Santosh Saxena
on 5/2/2021

"""
#Module Declaration
#-------------------------------------------------#
import os
import re
import sys
import json
import shutil
import numpy as np  
#-------------------------------------------------#

class File_name_validation:
    def __init__(self, logger, path):

        try:
            """
            Constructor Initialized

            Input : logger  , path
            Output : N/A

            """


            self.path = path
            self.logger = logger
            self.logger.add_in_logs("NAM","file name validation")
            self.logger.add_in_logs("BEG","File name validation module Initialized")
            self.logger.add_in_logs("INF","related data is loaded from source of truth for validation")
            self.no_of_date = json.load(open(path+"/Source_of_Truth/File_validation.json","r"))["no_date"]
            self.no_of_day = json.load(open(path+"/Source_of_Truth/File_validation.json","r"))["no_day"]

        except Exception as e:
            self.logger.add_in_logs("ERR" , "File name validation in Initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def generate_directories(self):

        """
        This function will generate 2 directories which are -
        1) good data folder
        2) bad data folder

        Input : N/A
        Output : Good dataset and Bad Dataset directories generation

        """

        try:
            self.logger.add_in_logs("chk","generate directories process Initialized")
            self.logger.add_in_logs("chk","generate directory for good data initialized")
            self.logger.add_in_logs("inf","checking previous availablity of directory")
            if os.path.isdir(self.path+"/Good_Dataset"):
                self.logger.add_in_logs("inf","directory with same name exists")
                self.logger.add_in_logs("inf","deleting previous directory")
                shutil.rmtree(self.path + "/Good_Dataset")
            os.mkdir(self.path + "/Good_Dataset")
            self.logger.add_in_logs("pas","generate directory for good data completed")
            
            self.logger.add_in_logs("chk","generate directory for bad data initialized")
            self.logger.add_in_logs("inf","checking previous availablity of directory")
            if os.path.isdir(self.path+"/Bad_Dataset"):
                self.logger.add_in_logs("inf","directory with same name exists")
                self.logger.add_in_logs("inf","deleting previous file")
                shutil.rmtree(self.path + "/Bad_Dataset")
            os.mkdir(self.path + "/Bad_Dataset")
            self.logger.add_in_logs("pas","generate directory for bad data completed")
            self.logger.add_in_logs("pas","generate directories process Completed")

        except Exception as e:
            self.logger.add_in_logs("ERR" , "file name validation in generate directories  ")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    def file_structure_checker(self, message):

        """
        This function will check the structure of file name are valid or not.
        
        Input : message
        Output : True/False i.e Boolean value

        """

        try:
            file_name = "['House']+['_']+['\d']+['_']+['\d']+[.csv]"
            if re.match(file_name , message):
                return True
            else:
                return False
        except Exception as e:
            self.logger.add_in_logs("ERR" , "file name validation in file structure checker")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def file_name_checker(self):

        """
        This function will check weather file name is valid according to Source_of_Truth or not
        
        Input : N/A
        Output : move data into good data and bad data with respect to validation conditions
        """
        try:
            self.logger.add_in_logs("chk","File name checker process Initialized")
            for i in os.listdir(self.path+"/Training_Batch_Folder"):
                file = i
                if self.file_structure_checker(i):
                    if(i[-4::1] == ".csv"):
                        i = i.split(".")[0]
                        i = i.split("_") 
                        if(i[0] == "House" and len(i[1]) == self.no_of_date and len(i[2]) == self.no_of_day):
                            self.logger.add_in_logs("inf",str(file) + " satisfiled all validations")
                            self.logger.add_in_logs("INF",str(file)+" is added in good data directory")
                            shutil.copy(self.path+"/Training_Batch_Folder/"+file, self.path+"/Good_Dataset")
                        else:
                            self.logger.add_in_logs("INF",str(file)+" is added in bad data directory")
                            self.logger.add_in_logs("INF",str(file)+" rejected because of slight changes")
                            shutil.copy(self.path+"/Training_Batch_Folder/"+file, self.path+"/Bad_Dataset")

                    else:
                        self.logger.add_in_logs("INF",str(file)+" is added in bad data directory")
                        self.logger.add_in_logs("INF",str(file)+" rejected because .csv is missing")                        
                        shutil.copy(self.path+"/Training_Batch_Folder/"+file , self.path+"/Bad_Dataset")

                else:
                    self.logger.add_in_logs("INF",str(file)+" is added in bad data directory")
                    self.logger.add_in_logs("INF",str(file)+" rejected because of irregular expression")
                    shutil.copy(self.path+"/Training_Batch_Folder/"+file , self.path+"/Bad_Dataset")
            
            self.logger.add_in_logs("pas","File name checker process Completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "file name validation in file name checker")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

        
    def file_name_validation_package(self):

        """
        This is the main body for file_valition
        
        Input : N/A
        Output : Name validation pipeline

        """
        try:
            self.generate_directories()
            self.file_name_checker()  
            self.logger.add_in_logs("END","File name validation module completed")  
        except Exception as e:
            self.logger.add_in_logs("ERR" , "file name validation in file name validation")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
