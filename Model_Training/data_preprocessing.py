"""
This class is used to do all sorts of required preprocessing from transformed data.

developed by : Santosh Saxena
on 19/4/2021

"""

#Module Declaration
#---------------------------------------------------------------------------#
import os
import sys
import kneed
import shutil
import pickle
import matplotlib
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder , StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
#---------------------------------------------------------------------------#

matplotlib.use("Agg")

class Data_preprocessing:

    def __init__(self,logger , path):
        try:
            """
            Constructor Initialized

            Input : Logger , path
            Output : N/A

            """
            self.path = path
            self.logger = logger
            self.df = pd.read_csv(path + "/Input_files/transformed_data.csv")
            self.logger.add_in_logs("Nam","Data Preprocessing")
            self.logger.add_in_logs("BEG","Data preprocessing module initialized")
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in Initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def generating_directories(self):
        
        try:
            """
            This function is used for generating direcotries 

            Input : N/A
            Output : Directories will be generated

            """
            self.logger.add_in_logs("chk","Generating directories process initialized")
            if(os.path.isdir(self.path + "/Model_files")):
                self.logger.add_in_logs("inf","Previous model files directory detected")
                self.logger.add_in_logs("inf","Deleting previos model files directory")
                shutil.rmtree(self.path + "/Model_files")
            self.logger.add_in_logs("inf","creating model files directory")
            os.mkdir(self.path + "/Model_files")
            self.logger.add_in_logs("inf","creating encoder directory")
            os.mkdir(self.path + "/Model_files/Encoder")
            self.logger.add_in_logs("inf","creating scaler directory")
            os.mkdir(self.path + "/Model_files/Scaler")
            self.logger.add_in_logs("inf","creating dimensionality reduction directory")
            os.mkdir(self.path + "/Model_files/Dimensionality_reduction")
            self.logger.add_in_logs("inf","creating cluster directory")
            os.mkdir(self.path + "/Model_files/Cluster_directory")
            self.logger.add_in_logs("inf","model directory is create")       
            os.mkdir(self.path + "/Model_files/Models")
            if(os.path.isdir(self.path + "/Input_files/Cluster_data")):
                self.logger.add_in_logs("inf","previous cluster directory detected")
                self.logger.add_in_logs("inf","deleting previous directory")
                shutil.rmtree(self.path + "/Input_files/Cluster_data")
            self.logger.add_in_logs("inf","creating cluster directory")
            os.mkdir(self.path + "/Input_files/Cluster_data")
            self.logger.add_in_logs("pas","generating directories process completed")

        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in generating directories")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def scaling(self):

        try:
            """
            The values with high scale will be standardize at a certain level in our dataset

            Input : N/A
            Output : values with high scale will be converted into a standard scaled values in out dataset


            """
            self.logger.add_in_logs("chk","Scaling process initialized")
            self.logger.add_in_logs("chk","Checking missing values for the last time")
            if(len(self.df.columns[self.df.isnull().sum() != 0]) == 0 ):
                self.logger.add_in_logs("pas","No Missing values")
            else:
                for i in self.df.columns[self.df.isnull().sum() != 0]:
                    self.logger.add_in_logs("inf", str(i) + " has missing values")
                self.logger.add_in_logs("pas","Data having missing values")
                raise("Data having missing values")
            
            sc = StandardScaler()
            column_names = list(self.df[self.df.columns[self.df.dtypes != "object"]].columns[self.df[self.df.columns[self.df.dtypes != "object"]].max() > 10])
            column_names.remove("SalePrice")
            file = open(self.path + "/Model_files/scaler_column.txt" , "w")
            temp = 0
            for i in column_names:
                file.write(str(i))
                temp += 1
                if(temp == len(column_names)):
                    continue
                else:
                    file.write(" ")
            file.close()
            self.df[column_names] = sc.fit_transform(self.df[column_names])
            self.logger.add_in_logs("inf","Values are scaled by standard scaler")
            self.logger.add_in_logs("inf","saving the scaler file in scaler directory")
            pickle.dump(sc , open(self.path+"/Model_files/Scaler/scaler.pickle","wb"))
            self.logger.add_in_logs("pas","scaling process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in scaling")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    def encoding(self):

        try:
            """
            The categorical values available in the dataset will be encoded

            Input : N/A
            Output : encoded values available in our dataset

            """

            self.logger.add_in_logs("chk","encoding process initialized")
            for i in self.df.columns[self.df.dtypes == "object"]:
                encoder = LabelEncoder()
                self.logger.add_in_logs("inf",str(i) + " is encoded")
                self.df[i] = encoder.fit_transform(self.df[i])
                self.logger.add_in_logs("inf",str(i) + " encoder file is saved in encoder directory")
                pickle.dump(encoder , open(self.path + "/Model_files/Encoder/"+str(i) + ".pickle","wb"))
            self.logger.add_in_logs("pas","encoder process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in encoding")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    
    def splitting_into_X_and_y(self):

        try:
            """
            Splitting our dataset into X and Y

            Input : N/A
            Output : X and y 

            """
            self.logger.add_in_logs("chk","Splitting data into x and y")
            self.X = self.df.drop(["SalePrice"] , axis = 1)
            self.y = self.df["SalePrice"]

        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in splitting into x and y")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

    
    def dimensionality_reduction(self):
        try:
            """
            If the dataset has high multi-collinearity it will be fixed with the dimensional reduction

            Input : N/A.
            Output : Dimensionally reduced dataset.

            """
            self.df.to_csv("/Users/santoshsaxena/Desktop/abcde.csv" , index = False)
            self.logger.add_in_logs("chk","Dimensionality Redction process Initialized")
            self.logger.add_in_logs("chk","find the number of dimension initialized")
            pca = PCA()
            temp = pca.fit_transform(self.df.drop(["SalePrice"], axis = 1))
            no_of_features = len(self.df.columns) - 1
            information = np.cumsum(pca.explained_variance_ratio_)
            number_of_dimensions = (information < 0.96).sum()
            self.logger.add_in_logs("inf",str(number_of_dimensions)+" is the number of dimensions required")
            self.logger.add_in_logs("pas","finding number of dimension complted")
            self.logger.add_in_logs("inf","ploting graph for dimensions vs evr")
            plt.figure()
            plt.style.use("classic")
            plt.plot(range(0, no_of_features) , information ,color = "blue", label = "information vs dimensions")
            plt.plot([number_of_dimensions, number_of_dimensions] ,[0,1] ,color = "black" ,label = "no_of_dimensions_used")
            plt.xlabel("Number of Dimensions")
            plt.ylabel("Information of Data")
            plt.legend(loc="lower left")
            plt.savefig(self.path + "/static/plots/Dimensions.jpg")
            self.logger.add_in_logs("inf","saving plot in plots directory")
            pca = PCA(n_components=number_of_dimensions)

            self.logger.add_in_logs("chk","Transforming data according to our dimensions")
            self.df = pca.fit_transform(self.df.drop(["SalePrice"], axis = 1))
            self.df = pd.DataFrame(self.df)
            self.df["SalePrice"] = self.y
            pickle.dump(pca, open(self.path+"/Model_files/Dimensionality_reduction/PCA.pickle","wb"))
            self.logger.add_in_logs("pas","Dimensionality Reduction Completed")
            self.logger.add_in_logs("pas","Demensionality reduction process completed")

        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in removing multi-collinearity")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
            
    def data_clustering(self):

        try:
            """
            Dataset is divided into clustes so similar data get trained in a particular model

            Input : N/A
            Output : Clusters will be generated and dataset will be stored in a particular directory
            """
            self.logger.add_in_logs("chk","Clustering process Initialized")
            self.logger.add_in_logs("chk","finding number of clusters")
            self.wcss = []
            x = self.df.drop(["SalePrice"], axis = 1)
            self.logger.add_in_logs("inf","saving a plot of wcss vs number of clusters ")
            for i in range(1,30):
                model = KMeans(n_clusters= i)
                model.fit(x)
                self.wcss.append(model.inertia_)
            k = kneed.KneeLocator(range(1,30),self.wcss,curve="convex", direction="decreasing")
            self.knee = k.knee
            self.logger.add_in_logs("inf",str(self.knee)+" number of clusters will be formed")
            self.wcss = np.array(self.wcss)/max(self.wcss)
            plt.figure()
            plt.style.use("classic")
            plt.plot(range(1,30), self.wcss , label = "WCSS vs Inertia", color = "blue")
            plt.plot([self.knee,self.knee],[min(self.wcss),1], label = "Number of cluster used", color = "black")
            plt.xlabel("No of cluster")
            plt.ylabel("WCSS")
            plt.legend(loc = "upper right")
            plt.savefig(self.path + "/static/plots/Cluster.jpg")
            self.logger.add_in_logs("pas","finding number of clusters completed")
            
            self.logger.add_in_logs("chk","getting cluster number for dataset")
            model = KMeans(n_clusters= self.knee)
            x = self.df.drop(["SalePrice"], axis = 1)
            model.fit(x)
            cluster_no = model.predict(x)
            self.df["Cluster"] = cluster_no
            self.logger.add_in_logs("inf","saving clustering model in model file")
            pickle.dump(model,open(self.path+"/Model_files/Cluster_directory/Cluster.pickle","wb"))

            for i in range(0,self.knee):
                self.logger.add_in_logs("inf", str(i) + " cluster is exported in .csv file")
                self.df[self.df["Cluster"] == i].to_csv(self.path + "/Input_files/Cluster_data/"+str(i)+"_cluster.csv", index = False)
            self.logger.add_in_logs("pas","Exporting Clustered dataset Completed")

            self.logger.add_in_logs("pas","Clustering process Completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in data clustering")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
        
    def data_preprocessing_package(self):
        try:
            """
            Data Preprocessing pipeline

            Input : N/A
            Output : N/A

            """
            self.generating_directories()
            self.scaling()
            self.encoding()
            self.splitting_into_X_and_y()
            self.dimensionality_reduction()
            self.data_clustering()
            self.logger.add_in_logs("END","Data Preprocessing module completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "data preprocessing in data clustering")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
            
    





            


