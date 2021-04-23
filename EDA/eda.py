"""
This class is used for exploratory data analysis.

developed by Santosh Saxena
on 19/4/2021
"""
#Module declaration
#------------------------------#
import os
import sys
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import matplotlib.pyplot as plt
#------------------------------#

class EDA_and_Transformation:

    def __init__(self,logger,path):
        try:

            """
            Constructor Initialized

            Input : Logger , path 
            Output : N/A

            """
            self.logger = logger
            self.path = path
            self.df = pd.read_csv(str(self.path)+"/Input_files/Input_data.csv")
            self.logger.add_in_logs("Nam","eda and transformation")
            self.logger.add_in_logs("BEG","EDA and Transformation module initialized")
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', -1)
            self.df[self.df.columns[self.df.dtypes == "object"]] = self.df[self.df.columns[self.df.dtypes == "object"]].replace(["NULL_values"], np.nan)
            self.df[self.df.columns[self.df.dtypes == "int"]] = self.df[self.df.columns[self.df.dtypes == "int"]].replace([9867], np.nan)
            self.df[self.df.columns[self.df.dtypes == "float"]] = self.df[self.df.columns[self.df.dtypes == "float"]].replace([9867.0], np.nan)
        except Exception as e:
            self.logger.add_in_logs("ERR" , "EDA in Initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    
    def generating_files(self):
        try:
            """
            Generating files for storing EDA results

            Input : N/A
            Output : Generating EDA files

            """
            self.logger.add_in_logs("chk","generating files process initialized")
            file = open(self.path + "/EDA/Metadata.txt","w")
            self.logger.add_in_logs("inf","file is generated with the name metadata.txt")
            file.write("\n" + " "*15 + "|¯¯¯¯¯¯¯¯¯¯¯¯¯|  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯|  |¯¯¯¯¯¯¯¯¯¯¯¯¯|")
            file.write("\n" + " "*15 + "|             |  |              |  |             |")
            file.write("\n" + " "*15 + "|   |¯¯¯¯¯¯¯¯¯    ¯¯|   |¯¯¯|   |  |   |¯¯¯¯¯|   |")
            file.write("\n" + " "*15 + "|   |               |   |   |   |  |   |     |   |")
            file.write("\n" + " "*15 + "|    ¯¯¯¯¯¯¯¯¯|     |   |   |   |  |    ¯¯¯¯¯    |")
            file.write("\n" + " "*15 + "|             |     |   |   |   |  |             |")
            file.write("\n" + " "*15 + "|   |¯¯¯¯¯¯¯¯¯      |   |   |   |  |   |¯¯¯¯¯|   |")
            file.write("\n" + " "*15 + "|   |_________    __|   |___|   |  |   |     |   |")
            file.write("\n" + " "*15 + "|             |  |              |  |   |     |   |")
            file.write("\n" + " "*15 + "|_____________|  |______________|  |___|     |___|")
            file.write("\n") 
            file.write("=="*50)
            file.close()
            self.logger.add_in_logs("pas","generating files process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "eda in generating files")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    
    def general_metadata(self):
        try:
            """
            Storing the meta data details of dataset in EDA files

            Input : N/A
            Output : EDA file with metadata

            """
            self.logger.add_in_logs("chk","general metadata process initialized")
            file = open(self.path + "/EDA/Metadata.txt","a")
            file.write("\n\n\n\n")
            self.logger.add_in_logs("inf","Adding general information of data in metadata")
            file.write("1) Data information\n")
            file.write("--"*50)
            file.write("\n")
            self.df.info(buf = file)
            file.write("\n\n\n\n")
            self.logger.add_in_logs("inf","Adding detailed description about data in metadata")
            file.write("2) Detailed description of continuous data\n")
            file.write("--"*50)
            file.write("\n")
            #file.write(str(self.df.describe()))
            for i in range(0,len(self.df.columns[self.df.dtypes != "object"]),7):
                file.write(str(self.df[self.df.columns[self.df.dtypes != "object"]].iloc[:,i:i+7].describe()))
                file.write("\n\n")
            file.write("\n\n\n\n")
            file.write("3) Detailed description of categorical data\n")
            file.write("--"*50)
            file.write("\n")
            for i in range(0,len(self.df.columns[self.df.dtypes == "object"]),7):
                file.write(str(self.df[self.df.columns[self.df.dtypes == "object"]].iloc[:,i:i+7].describe(include = "O")))
                file.write("\n\n")
            self.logger.add_in_logs("pas","general metadata process completed")
            file.close()
        except Exception as e:
            self.logger.add_in_logs("ERR" , "eda in general metadata")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    def missing_values(self):
        try:
            """
            Finding the missing values of dataset and storing it in the EDA file

            Input : N/A
            Output : EDA file with missing value details

            """
            self.logger.add_in_logs("chk","missing value process initialized")
            file = open(self.path + "/EDA/Metadata.txt","a")
            file.write("\n\n")
            file.write("4)Features having missing values\n")
            file.write("--"*50)
            file.write("\n")
            self.logger.add_in_logs("inf","finding features having missing features")
            file.write(str(self.df[self.df.dtypes.index[self.df.isnull().sum() !=0]].isnull().sum()))
            self.logger.add_in_logs("inf","Adding the missing values details in metadata")
            self.logger.add_in_logs("pas","missing value process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "eda in missing value")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    
    
    def handling_missing_values(self):

        try:
            """
            Handling the features who has missing values 

            Input : N/A
            Output : No missing values in dataset

            """

            self.logger.add_in_logs("chk","handling missing values process initialized")
            for i in self.df.columns:
                if(self.df[i].isnull().sum() == 0):
                    continue 
                else:
                    self.logger.add_in_logs("inf", i + " has missing values")
                    if(self.df[i].dtype == "object"):
                        self.logger.add_in_logs("inf",i + " is a categorical feature")
                        if(self.df[i].isnull().sum() >= 0.5 * len(self.df)):
                            self.logger.add_in_logs("inf", i + " removing because too many missing values")
                            self.df.drop([i], axis = 1 , inplace = True )
                        else:
                            self.logger.add_in_logs("inf" , i + " missing values handled by imputed with ffill method")
                            self.df[i].fillna("ffill" , inplace = True)
                    if(self.df[i].dtype != "object"):
                        self.logger.add_in_logs("inf", i + " is a continuous feature")
                        if(self.df[i].isnull().sum() >= 0.9 * len(self.df)):
                            self.logger.add_in_logs("inf", i + " removing because too many missing values")
                            self.df.drop([i] , axis = 1 , inplace = True)
                        else:
                            self.logger.add_in_logs("inf", i + " missing values handled by imputing mean of a feature")
                            self.df[i].fillna(value = self.df[i].mean(), inplace = True)
            self.df.to_csv(self.path + "/Input_files/Dataset.csv" , index = False)
            self.logger.add_in_logs("inf", "Dataset is exported in a input directory")
            self.logger.add_in_logs("pas","handling missing values process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "eda in handling missing value")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    
    def export_transformed_data(self):
        try:
            """
            Exporting all the transformed data up till now in Input file to use it later

            Input : N/A
            Output : Dataframe in a form of csv file in Input file directory.
            """

            self.logger.add_in_logs("chk", "export transformed data process initialized")
            self.logger.add_in_logs("chk","Exporting transformed data into .csv file")
            self.df.drop("Id",axis = 1 , inplace = True)
            self.df.to_csv(self.path + "/Input_files/transformed_data.csv", index = False)
            self.logger.add_in_logs("pas","Exporting transformed data completed")
            self.logger.add_in_logs("pas","Export transformed data process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "eda in export tansformed data")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def eda_transformation_package(self):
        try:

            """
            EDA Pipeline. All the functions integrated with one function 

            Input : N/A
            Output : Integration and creation of pipeline  
            """
            self.generating_files()
            self.general_metadata()
            self.missing_values()
            self.handling_missing_values()
            self.export_transformed_data()
            self.logger.add_in_logs("end","EDA and transformation module completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "eda in general metadata")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
            
