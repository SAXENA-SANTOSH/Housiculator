"""
This is a training module all the AI training module is integrated to this module and this module is routed to the main application

Developed by : Santosh Saxena
"""

# Module Declaration
#----------------------------------------------------------------#
import os
import sys
import pandas as pd
from EDA.plots import Plots
from Logger.logger import Logger
from EDA.eda import EDA_and_Transformation
from Data_Validation.database import Database 
from Model_Training.model_training import ML_model 
from Data_Validation.file_name import File_name_validation
from Data_Validation.data_validation import Data_validation 
from Model_Training.data_preprocessing import Data_preprocessing
#----------------------------------------------------------------#

class Training:
    def train(self,path , data_base_name , data_base_table_name):
        try:
            """
            All the packages related to AI modules are called and pipeline is created

            Input : Path , Database name , Database table name
            Output : AI Model file , related model files and various evaluation metrics etc
            """  
            logger = Logger(path)
            logger.generate_metadata_logs()
            file_validation = File_name_validation(logger, path).file_name_validation_package()
            data_validation = Data_validation(logger, path).data_validation_package()
            database = Database(logger,path,data_base_name,data_base_table_name).database_package()
            exploratory_data_analysis = EDA_and_Transformation(logger,path).eda_transformation_package()
            plots = Plots(logger , path).plots_package()
            data_preprocessing = Data_preprocessing(logger,path).data_preprocessing_package()
            machine_learning_model_accuracy = ML_model(logger ,path).ML_training_package()
            return machine_learning_model_accuracy
        except Exception as e:
            self.logger.add_in_logs("ERR" , "Training module")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

