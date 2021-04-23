"""
This class will find the individual model for all clusters. The model with higher accuracy will be selected and 
saved in a particular directory

Written by : Santosh Saxena
on 17/2/2021

"""
#Module declaration
#-------------------------------------------------------------------------#
import os
import sys
import shutil
import pickle
import numpy as np
import pandas as pd
import matplotlib
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression , Ridge , Lasso
from sklearn.model_selection import GridSearchCV , train_test_split
from sklearn.ensemble import BaggingRegressor , RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor , GradientBoostingRegressor 
#--------------------------------------------------------------------------#
matplotlib.use("Agg")

class ML_model:

    def __init__(self, logger , path):
        """
        ML Model is initialized

        Input : N/A
        Output : N/A

        """
        self.path = path
        self.logger = logger
        self.accuracy = []
        self.random_state = 101
        self.model = [LinearRegression() , SVR() , DecisionTreeRegressor()]
        self.ensemble = [BaggingRegressor(),RandomForestRegressor(), AdaBoostRegressor(), 
                        GradientBoostingRegressor(), XGBRegressor()]

    def separating_df_into_x_y(self, df):
        
        """
        This function will separate the dataset into X and y dataframe

        Input df i.e Dataframe
        Output X and y i.e Dataframe
        """
        try:
            self.logger.add_in_logs("Chk","Separating data into X and y process Initialized")
            self.X = df.drop(["Cluster","SalePrice"], axis = 1)
            self.y = df["SalePrice"]
            self.x_train, self.x_test , self.y_train, self.y_test = train_test_split(self.X, self.y, test_size = 0.25 , random_state = self.random_state)
            self.logger.add_in_logs("pas","Separating data into X and y process Completed")

        except Exception as e:
            self.logger.add_in_logs("ERR" , "ML training in separating into x and y")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    def model_selection(self):

        """
        This function will select model

        Input: N/A
        Output: model index i.e int
        """

        try:
            self.logger.add_in_logs("Chk","Model Selection process Initialized")
            accuracy = []
            for i in self.model:
                model = i
                model.fit(self.x_train, self.y_train)
                accuracy.append(model.score(self.x_test, self.y_test))

            for i in range(len(accuracy)):
                if(accuracy[i] == max(accuracy)):
                    self.logger.add_in_logs("pas","Model Selection process Completed")
                    return i

        except Exception as e:
            self.logger.add_in_logs("ERR" , "ml training in model selection")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
        
    def get_max_model(self ,df):

        """
        This function will find the best possible parameters of our selected model

        Input: model index
        OutPut: tunning model 
        """
        
        try:
            self.df = df
            self.logger.add_in_logs("Chk", "Selecting best model process Initialized")
            self.separating_df_into_x_y(self.df)
            model = self.model_selection()
            self.decison_tree = False
    
            if(model == 0):
                self.logger.add_in_logs("inf","Linear Regression model is base model")
                self.trail_model = LinearRegression()
                self.parameters = {
                                    }
            if(model == 1):
                self.logger.add_in_logs("inf","SVR model is base model")
                self.trail_model = SVR()
                self.parameters = {
                                "kernel":["linear","poly","rbf","sigmoid"],
                                "gamma":["scale", "auto"],
                                }
        
            if(model == 2):
                self.logger.add_in_logs("inf","decision tree model is base model")
                self.trail_model = DecisionTreeRegressor()
                self.parameters = {
                                "criterion": ["mse", "friedman_mse", "mae"],
                                "splitter": ["best", "random"]
                                }
                self.decison_tree = True
            self.logger.add_in_logs("chk","hyper-parameter tunning initialized")
            self.gs = GridSearchCV(estimator = self.trail_model, param_grid= self.parameters, verbose = 3)
            self.gs.fit(self.X, self.y)
            self.logger.add_in_logs("pas","hyper-paramenter tunning completed")
            self.logger.add_in_logs("pas","Selecting best model process Completed")
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "ml training in get max model")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
        
    def ensemble_selection_and_exporting(self,k):

        """
        More tunning by adding ensemble approach to model and selecting the best possible model
        
        Input : previous model i.e trail model
        Output: Final model and that to saving in a directory
        """

        try:  
            self.logger.add_in_logs("Chk","Ensemble selection process Initialized") 
            accuracy = []
            self.final_model = []


            final_model = self.trail_model
            final_model = self.trail_model.set_params(**self.gs.best_params_)
            final_model.fit(self.x_train, self.y_train)
            accuracy.append(final_model.score(self.x_test, self.y_test))
            
            final_model = BaggingRegressor(base_estimator = final_model)
            final_model.fit(self.x_train, self.y_train)
            accuracy.append(final_model.score(self.x_test, self.y_test))

            final_model = AdaBoostRegressor(base_estimator = final_model)
            final_model.fit(self.x_train, self.y_train)
            accuracy.append(final_model.score(self.x_test, self.y_test))

            final_model = GradientBoostingRegressor()
            final_model.fit(self.x_train, self.y_train)
            accuracy.append(final_model.score(self.x_test, self.y_test))
        
            final_model = XGBRegressor(base_estimator = final_model)
            final_model.fit(self.x_train, self.y_train)
            accuracy.append(final_model.score(self.x_test, self.y_test))

            final_model= self.trail_model
            final_model.fit(self.x_train, self.y_train)
            accuracy.append(final_model.score(self.x_test, self.y_test))


            if(self.decison_tree):
                final_model = RandomForestRegressor()
                final_model.fit(self.x_train, self.y_train)
                accuracy.append(final_model.score(self.x_test, self.y_test))

            for i in range(len(accuracy)):
                if(accuracy[i] == max(accuracy)):
                    model_no = i


            if(model_no == 0):
                final_model = final_model
                final_model.fit(self.X, self.y)
                
            if(model_no == 1):
                final_model = BaggingRegressor(base_estimator = final_model)
                final_model.fit(self.X, self.y)

            if(model_no == 2):
                final_model = AdaBoostRegressor(base_estimator = final_model)
                final_model.fit(self.X, self.y)

            if(model_no == 3):
                final_model = GradientBoostingRegressor()
                final_model.fit(self.X, self.y)

            if(model_no == 4):
                final_model = XGBRegressor(base_estimator = final_model)
                final_model.fit(self.X, self.y)

            if(model_no == 5):
                final_model = self.trail_model
                final_model.fit(self.X, self.y)         
        
            if(model_no == 6):
                final_model = RandomForestRegressor()
                final_model.fit(self.X, self.y)

            pickle.dump(final_model, open(self.path  + "/Model_files/Models/Model_"+str(k) + "_cluster.pickle" , "wb"))
            f_m = str(final_model)
            f_m = f_m.split("(")[0]
            self.logger.add_in_logs("inf",str(f_m) + " model is selected for cluster " + str(k) )
            acc = final_model.score(self.x_test , self.y_test)
            self.logger.add_in_logs("inf",str(acc)+" is the accuracy")
            self.logger.add_in_logs("pas","Ensemble selection and exporting process Completed")
            return max(accuracy)
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "ml training in ensemble selection and exporting")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def ML_training_package(self):
        """
        This function is used to create a pipeline of all above functions

        Input : N/A
        Output : N/A
        """
        try:
            self.logger.add_in_logs("NAM","ML Model")
            self.logger.add_in_logs("BEG","ML training process Initialized")
            temp = 0
            accuracy = []
            for i in os.listdir(self.path + "/Input_files/Cluster_data/"):
                temp += 1
                df = pd.read_csv(self.path + "/Input_files/Cluster_data/" + str(i)) 
                self.get_max_model(df)
                accuracy.append(round(self.ensemble_selection_and_exporting(temp),2)*100)
            mean_accuracy  = np.mean(accuracy)
            accuracy = np.array(accuracy)
            self.logger.add_in_logs("inf" , "saving accuracy in files")
            cluster = list(range(0 , len(accuracy)))
            accuracy_df = pd.DataFrame({"Cluster" : cluster , "Accuracy":accuracy})
            accuracy_df.index = accuracy_df["Cluster"]
            accuracy_df.drop(["Cluster"] , axis = 1 , inplace = True)
            file = open(self.path + "/static/accuracy.txt","w")
            file.write("\n")
            file.write(str(accuracy_df))
            file.close()

            if(os.path.isdir(self.path + "/static/accuracy_plot")):
                shutil.rmtree(self.path + "/static/accuracy_plot")
            os.mkdir(self.path + "/static/accuracy_plot")
                
            plt.figure()
            plt.style.use("classic")
            plt.plot(cluster , accuracy , label = "Accuracy")
            plt.scatter(len(cluster)//2 , mean_accuracy , label = "Mean Accuracy")
            plt.xlabel("Cluster number")
            plt.ylabel("Model Accuracy")
            plt.title("Accuracy")
            plt.grid(True)
            plt.legend()
            plt.savefig(self.path + "/static/accuracy_plot/line_accuracy.png")
        
            plt.figure()
            plt.style.use("classic")
            plt.bar(cluster , accuracy , label = "Accuracy")
            plt.xlabel("Cluster number")
            plt.ylabel("Model Accuracy")
            plt.title("Accuracy")
            plt.grid(True)
            plt.legend()
            plt.savefig(self.path + "/static/accuracy_plot/bar_accuracy.png")
            
            self.logger.add_in_logs("inf", str(mean_accuracy) + " is the overall accuracy")
            self.logger.add_in_logs("end","ML Training Module Completed")
            return mean_accuracy
        except Exception as e:
            self.logger.add_in_logs("ERR" , "ml training in package")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
