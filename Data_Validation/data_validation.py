"""
This Class will check the data available in files. The major criteria of validation data in the files are -

1) Columns data validation
2) number of row validation
3) data type of features validation
4) unique categorical values from categorical feature

If the data available in the files satisfies these criteria then only it will be remained in the good data
else that file will be moved to bad dataset

developed by : Santosh Saxena
on 8/2/2021
"""
#Module declaration
#----------------------------------------------------#
import os
import sys
import json
import shutil
import pandas as pd
#----------------------------------------------------#

class Data_validation:
    def __init__(self,logger ,path):
        try:

            """
            Constructure Initialized

            Input : path , logger
            Output : N/A

            """

            self.logger = logger
            self.path = path
            self.logger.add_in_logs("NAM","Data Validation")
            self.logger.add_in_logs("BEG","Data Validation module Initialized")
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Data Validation in Initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))



    def loading_sot(self):

        """
        This function will load the Source of Truth to compare with our dataset

        Input : N/A
        Output : SOT files dataframe or dictionary 
        """

        try:
            self.logger.add_in_logs("inf","related data is loaded from source of truth for validation")
            self.logger.add_in_logs("chk","loading source of truth process initialized")
            column = open(self.path+"/Source_of_Truth/Data_columns.txt","r")
            self.column = column.read().split(",")
            column.close()
            self.categorical_unique_values = json.load(open(self.path+"/Source_of_Truth/Data_categorical.json","r"))
            self.file_validation = json.load(open(self.path+"/Source_of_Truth/File_validation.json","r"))
            self.datatype = pd.read_csv(self.path+"/Source_of_Truth/Data_type.csv", index_col="Unnamed: 0")
            self.logger.add_in_logs("pas","Loading Source of Truth process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Data validation in loading_sot")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def unique_categorical_values(self, df):

        """
        This function will check if any random categorical values are there which are not present in the Source of Truth at 
        that time that dataset will move to towards bad dataset

        Input : Dataframe
        Output : fault : Int

        """
        try:
            fault = 0
            for i in df.columns[df.dtypes == "object"]:
                cat_sot_values = set(self.categorical_unique_values[i])
                cat_df_values = set(pd.Categorical(df[i]).categories)
                if(cat_df_values.issubset(cat_sot_values)):
                    continue
                else:
                    fault += 1
            return fault
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Data validation in unique categorical values")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    def data_type_validation(self, df):

        """
        This function will check the data types of the comming data with respect to the Source_of_Truth
        
        Input : Dataframe
        Output : fault : Int 
        
        """
        
        try:
            fault = 0
            for i in df.columns:
                if(df[i].dtypes == self.datatype.loc[i]["SOT"]):
                    continue
                else:
                    fault += 1

            return fault
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Data validation in data type validation")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))



    def data_checker(self):

        """
        If all the condition are satisfied then only it will be in the present in the good dataset 
        else that file will be moved to bad data folder
        
        Input : N/A
        Output : Data files will move towards good and bad directory 

        """

        self.logger.add_in_logs("Chk","Data checking process Initialized")
        try:
            for i in os.listdir(self.path+"/Good_Dataset/"):
                df = pd.read_csv(self.path+"/Good_Dataset/"+i)
                if(list(df.columns) != self.column):
                    self.logger.add_in_logs("inf", str(i) + " shifted to bad data directory")
                    self.logger.add_in_logs("inf",str(i) + " rejected because of columns")
                    shutil.move(self.path+"/Good_Dataset/"+i , self.path+"/Bad_Dataset/"+i)
                elif(len(df) != self.file_validation["no_of_rows"]):
                    self.logger.add_in_logs("inf", str(i) + " shifted to bad data directory")
                    self.logger.add_in_logs("inf", str(i) + " rejected because of rows")
                    shutil.move(self.path+"/Good_Dataset/"+i , self.path+"/Bad_Dataset/"+i)
                elif(self.data_type_validation(df) != 0):
                    self.logger.add_in_logs("inf", str(i) + " shifted to bad data directory")
                    self.logger.add_in_logs("inf", str(i) + " rejected because of data type")
                    shutil.move(self.path+"/Good_Dataset/"+i , self.path+"/Bad_Dataset/"+i)
                elif(self.unique_categorical_values(df) != 0):
                    self.logger.add_in_logs("inf", str(i) + " shifted to bad data directory")
                    self.logger.add_in_logs("inf", str(i) + " rejected because of unique categories")
                    shutil.move(self.path+"/Good_Dataset/"+i , self.path+"/Bad_Dataset/"+i)
                else:
                    self.logger.add_in_logs("inf",str(i) + " satisfiled all validations")
                    self.logger.add_in_logs("inf",str(i) + " stayed in good data directory")
                    continue
            self.logger.add_in_logs("Pas","data checking process Completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Data validation in data checker")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def data_validation_package(self):
        """
        This is the main body for file_data_validation
        
        Input : N/A
        Output : Pipeline
        
        """
        try:
            self.loading_sot()
            self.data_checker()
            self.logger.add_in_logs("END","Data validation module completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Data validation in data validation package")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

        
        





            

                
