"""
This Module is used for prediction 

Developed by Santosh Saxena 
on 24/4/2021

"""

# Module declaration
#------------------#
import re
import sys
import os
import json
import shutil
import pickle
import numpy as np 
import pandas as pd 
#-------------------#

class Prediction:
    def __init__(self,path , file_path , runtime_logger):
        try:
            """
            Prediction Module Initialization 

            Input : path , file path , runtime logger
            Output : N/A

            """
            self.path = path
            self.file_path = file_path
            self.runtime_logger = runtime_logger
            self.condition = True
            self.file_name = self.file_path.split("/")[-1]
            self.df = pd.read_csv(file_path)
            self.categorical_unique_values = json.load(open(self.path+"/Source_of_Truth/Data_categorical.json","r"))
            self.no_of_date = json.load(open(path+"/Source_of_Truth/File_validation.json","r"))["no_date"]
            self.no_of_day = json.load(open(path+"/Source_of_Truth/File_validation.json","r"))["no_day"]
            column = open(self.path+"/Source_of_Truth/Data_columns.txt","r")
            self.column = column.read().split(",")
            self.cluster = pickle.load(open(self.path + "/Model_files/Cluster_directory/Cluster.pickle", "rb"))
            self.pca = pickle.load(open(self.path + "/Model_files/Dimensionality_reduction/PCA.pickle", "rb"))
            self.sc_x = pickle.load(open(self.path + "/Model_files/Scaler/scaler.pickle","rb"))
            self.datatype = pd.read_csv(self.path+"/Source_of_Truth/Data_type.csv", index_col="Unnamed: 0")
            self.datatype.drop(["SalePrice"] , inplace = True)
            self.file_validation = json.load(open(self.path+"/Source_of_Truth/File_validation.json","r"))
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error")
            self.runtime_logger.add_in_logs("Path is not correct")


    def file_structure_checker(self, message):

        """
        This function will check the structure of file name are valid or not.

        Input : Message
        Output : True/False , Boolean value

        """

        try:
            file_name_expression = "['House']+['_']+['\d']+['_']+['\d']+[.csv]"
            if re.match(file_name_expression , message):
                return True
            else:
                return False
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error in code")
            self.runtime_logger.add_in_logs("Prediction in file structure checker")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))

    def name_validations(self):
        try:
            """
            This function will validation the given file on the basis of name. If passed then moved further validations
            or prediction will not be done .

            Input : N/A
            Output : our variable i.e self.condition value will be decided

            """
            i = self.file_name
            if self.file_structure_checker(i):
                if(i[-4::1] == ".csv"):
                    i = i.split(".")[0]
                    i = i.split("_") 
                    if(i[0] == "House" and len(i[1]) == self.no_of_date and len(i[2]) == self.no_of_day):
                        self.runtime_logger.add_in_logs("File name is matched with requirements")
                    else:
                        self.condition = False
                        self.runtime_logger.add_in_logs("Faced an error")
                        self.runtime_logger.add_in_logs("File not matched with requirements")
                else:
                    self.condition = False
                    self.runtime_logger.add_in_logs("Faced an error")
                    self.runtime_logger.add_in_logs("File not matched with requirements")
            else:
                self.condition = False
                self.runtime_logger.add_in_logs("Faced an error")
                self.runtime_logger.add_in_logs("File not matched with requirements")
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error in code")
            self.runtime_logger.add_in_logs("Prediction in name validation")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))

    def data_type_validation(self, df):

        """
        This function will check the data types of the comming data with respect to the Source_of_Truth
        
        Input : Dataframe
        Ouput : fault , Integer

        """
        
        try:
            fault = 0
            for i in self.df.columns:
                if(self.df[i].dtypes == self.datatype.loc[i]["SOT"]):
                    continue
                else:
                    fault += 1

            return fault
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error")
            self.runtime_logger.add_in_logs( "Data validation in data type validation")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))


    def unique_categorical_values(self, df):

        """
        This function will check if any random categorical values are there which are not present in the Source of Truth at 
        that time that dataset will move to towards bad dataset

        Input : Dataframe
        Output : fault , Integer

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
            self.runtime_logger.add_in_logs("Faced an error")
            self.runtime_logger.add_in_logs("Data validation in unique categorical values")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))



    def data_validation(self):
        try:
            """
            This function will validate the prediction file on the basis of data available in the file
            If all the validation conditions are satisfied then only it will be predicted
            
            Input : N/A
            Output : self.condition valriable value will be decided
            
            """

            self.column.remove("SalePrice")
            if(list(self.df.columns) != self.column):
                self.condition = False
                self.runtime_logger.add_in_logs("Data columns not matched the standard requirements")
            elif(len(self.df) != self.file_validation["no_of_rows"]):
                self.condition = False
                self.runtime_logger.add_in_logs("Data number of rows not matched the standard requirements")
            elif(self.data_type_validation(self.df) != 0):
                self.condition = False
                self.runtime_logger.add_in_logs("Data type not matched the standard requirements")
            elif(self.unique_categorical_values(self.df) != 0):
                self.condition = False
                self.runtime_logger.add_in_logs("Categories not matched the standard requirements")
            else:
                self.runtime_logger.add_in_logs("Data is matched with the requirements")
            
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error")
            self.runtime_logger.add_in_logs("Prediction in Data Validation")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))

    def prediction(self):
        try:
            """
            The main prediction function . After passing through all the validation this function wil predict
            the dataset sent by the user

            Input : N/A
            Output : predicted value dataframe

            """
            if(len(self.df.columns[self.df.isnull().sum() != 0]) > 0):
                self.runtime_logger.add_in_logs("Data has missing values")
            else:
                self.runtime_logger.add_in_logs("Data has no missing values")
                x = self.df.copy()
                file = open(self.path + "/Model_files/scaler_column.txt","r")
                column = str(file.read()).split(" ")
                x[column] = self.sc_x.transform(x[column])
                for i in os.listdir(self.path + "/Model_files/Encoder/"):
                    encoder = pickle.load(open(self.path + "/Model_files/Encoder/" + str(i) , "rb"))
                    name = i.split("/")[-1]
                    name = name.split(".")[0]
                    x[name] = encoder.transform(x[name])
                x.drop(["Id"], axis = 1 , inplace = True)
                result = self.pca.transform(x)
                result = pd.DataFrame(result)
                cluster_no = self.cluster.predict(result)
                prediction = []
                for i in range(len(cluster_no)):
                    if(os.path.isfile(self.path + "/Model_files/Model_"+str(cluster_no[i])+"_cluster.pickle")):
                        ML_model = pickle.load(open(self.path + "/Model_files/Models/Model_"+str(cluster_no[i])+"_cluster.pickle", "rb"))
                        prediction.append(round(ML_model.predict(pd.DataFrame(result.iloc[i]).transpose())[0], 2))
                    else:
                        ML_model = pickle.load(open(self.path + "/Model_files/Models/Model_"+str(2)+"_cluster.pickle", "rb"))
                        prediction.append(round(ML_model.predict(pd.DataFrame(result.iloc[i]).transpose())[0], 2))

                self.df["SalePrice"] = prediction
            
                if(os.path.isdir(self.path + "/Prediction/Predicted_Data")):
                    self.df.to_csv(self.path + "/Prediction/Predicted_Data/"+str(self.file_name) , index = False)
                    self.runtime_logger.add_in_logs("Predicted file is generated")
                else:
                    os.mkdir(self.path + "/Prediction/Predicted_Data")
                    self.df.to_csv(self.path + "/Prediction/Predicted_Data/"+str(self.file_name) , index = False)
                    self.runtime_logger.add_in_logs("Predicted file is generated")

            
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error")
            self.runtime_logger.add_in_logs("Prediction in Prediction")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))


    def prediction_package(self):
        try:
            print(self.df.dropna(inplace = True))
            self.name_validations()
            self.data_validation()
            if(self.condition):
                self.prediction()
            else:
                raise("Does not satisfied validations")
        except Exception as e:
            self.runtime_logger.add_in_logs("Faced an error")
            self.runtime_logger.add_in_logs("Prediction in prediction package")
            self.runtime_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.runtime_logger.add_in_logs(str(e))
