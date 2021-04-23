"""
This class will set a database and create a table for our dataset. After inserting all the observations in the database
that table will be exported to .csv file and will be stored in input file with the name of Input_data.csv. 

Developed by Santosh Saxena 
on 11/12/2020


"""


#Module Declaration
#-----------------------#
import os
import sys
import shutil
import mysql.connector
import numpy as np
import pandas as pd
#-----------------------#

class Database:

    def __init__(self, logger , path, database_name, table_name):

        try:    
        
            """
            Constructure Initialized

            Input : Logger , path , database name , table name
            Output : N/A


            """

            self.path = path
            self.logger = logger
            self.db_name = database_name.lower()
            self.table_name = table_name
            self.columns = pd.read_csv(self.path+"/Source_of_Truth/Data_type.csv").iloc[:,0]
            self.dtypes = []
        
            self.logger.add_in_logs("NAM" , "Database")
            self.logger.add_in_logs("BEG","Database insertion module Initialized")

            df = pd.read_csv(self.path+"/Source_of_Truth/Data_type.csv")
            for i in df.iloc[:,1]:
                if(i == "int64"):
                    self.dtypes.append("int")
                if(i == "float64"):
                    self.dtypes.append("float")
                if(i == "object"):
                    self.dtypes.append("varchar")
            self.logger.add_in_logs("INF","Related data is loaded from source of truth")

        except Exception as e:
            self.logger.add_in_logs("ERR" , "Database in Initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def database_connectivity(self):
        
        """
        This function will create a database
        
        Input : N/A
        Output : Database 
        """

        try:
            self.logger.add_in_logs("chk","Database setup connectivity process Initialized")
            # Enter the database details
            db = mysql.connector.connect(
                 host ='localhost',         
                 user = 'root',
                 password = 'Santoshkyn14@'
            )
            if(db):
                self.logger.add_in_logs("inf","System connected to database")
            else:
                raise("System database connection failed")

            self.logger.add_in_logs("INF","Cursor for database is initialized")
            cursor = db.cursor(buffered=True)
            cursor.execute("show databases")
            exist_db = False
            self.logger.add_in_logs("inf","checking previous availablity of database")
            for i in cursor:
                if(i[0].lower() == self.db_name):
                    exist_db = True
                    break
                else:
                    continue

            if(exist_db):
                self.logger.add_in_logs("INF","Previous database detected")
                self.logger.add_in_logs("inf","Deleting previous database")
                cursor.execute("drop database "+str(self.db_name))
            self.logger.add_in_logs("chk","Creating a database named "+str(self.db_name))
            cursor.execute("create database  "+ str(self.db_name))

            self.logger.add_in_logs("pas","Database creation process completed")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in database connectivity")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def create_table(self, mycursor ,table_name , columns , columns_type , num , features = [], primary_key = [], foreign_key = [], reference = []):
        """
        This is a function to generate a query for creating a table

        Input : basic inputs to generate queries
        Output : Table in database

        """
        
        
        try:
            if(columns == [] or columns_type == [] and mycursor == ""):
                raise("ERR","attributes are missing")
            else:
                string = "create table if not exists " + table_name + "("
                for i,j,k in zip(columns, columns_type, num):
                    if(j == "float"):
                        k = ""
                    else:
                        k = "("+str(k) +")"
                    string = string + i+" "+j  + str(k) 
                    if(features != []):
                        string = string + features.pop(0) + ","
                    else:
                        string = string + ","
                if(primary_key != []):
                    string = string + "primary key(" + primary_key.pop(0) + ")," 
                for i,j in zip(foreign_key, reference):
                    string = string + "foreign key (" + i + ") " + "references " + j+","
                string = string[0:len(string) - 1]
                string = string + ")"
                mycursor.execute(string)
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in create table")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def insert_into_table(self, mycursor,table_name=[], values=[]):
        """
        This is a function to generate a query for insertion of observation into database table 

        Input : observations to add in database
        Output : observation in a database table
        """
        
        try:
            if(table_name == [] or values == []):
                raise("parameters of table are missing")
            else:
                string = "insert into "+table_name 
                mycursor.execute("desc " + table_name)
                string = string + "("
                for i in mycursor:
                    string = string + i[0] +","
                string = string[0: len(string) - 1]
                string = string + ")"
                string = string + " values("
                for i in values:
                    if(type(i) == str):
                        string = string + "'"
                        string = string + "{}".format(i)
                        string = string + "',"
                    else:
                        string = string + "{}".format(i)
                        string = string + ","
                string = string[0:len(string)-1]
            string = string + ")"
            mycursor.execute(string)
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in insert into table")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))




    def table_creation(self):

        """
        This function will create table in database

        Input : N/A
        Output : Database table creation function call
        """

        try:
            self.logger.add_in_logs("chk","table creation process initialized")
            # Database credentials
            self.db = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "Santoshkyn14@",
                database = self.db_name
            )
            if self.db:
                self.logger.add_in_logs("inf","Created database connected")
            else:
                raise("connection to database failed")

            self.cursor = self.db.cursor()
            exist_table= False
            self.cursor.execute("show tables")
            for i in self.cursor:
                if(i[0] == self.table_name):
                    exist_table = True
                    break
                else:
                    continue

            self.logger.add_in_logs("Chk","previous availablity of table")
            
            if(exist_table):
                self.logger.add_in_logs("INF" ,"previous table detected")
                self.logger.add_in_logs("INF" , "deleting previous table")
                self.cursor.execute("drop table "+ str(self.table_name))
            
            self.logger.add_in_logs("chk","table creation initialized with name "+str(self.table_name))
            self.create_table(self.cursor ,self.table_name , 
            list(self.columns),
            list(self.dtypes),
            [100]*len(self.columns)
            )    
            self.logger.add_in_logs("pas","Table Created process Successfully")
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in table creation")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    
    def inserting_into_database(self):

        """
        This function will insert observations into database tables

        Input : N/A
        Output : Inserting obeservations into database table function call 

        """
        try:
            self.logger.add_in_logs("Chk","Insertion of data into database process Initialized")
            for i in os.listdir(self.path+"/Good_Dataset/"):
                df = pd.read_csv(self.path+"/Good_Dataset/"+i)
                df[df.columns[df.dtypes == "int"]] = df[df.columns[df.dtypes == "int"]].fillna(value= 9867)
                df[df.columns[df.dtypes == "float"]] = df[df.columns[df.dtypes == "float"]].fillna(value = 9867.0)
                df[df.columns[df.dtypes == "object"]] = df[df.columns[df.dtypes == "object"]].fillna(value= "NULL_values")
                for j in range(len(df)):
                    self.insert_into_table(mycursor = self.cursor,table_name= self.table_name,values=list(df.iloc[j]))
                self.logger.add_in_logs("INf",str(i) + " is added into database")
            self.logger.add_in_logs("pas","Insertion of data on database is Completed")
            self.logger.add_in_logs("Chk", "Exporting to .csv Initialized")

            self.logger.add_in_logs("inf","Fetching all data from database")
            self.cursor.execute("select * from "+self.table_name)
            input_data = self.cursor.fetchall()

            self.db.commit()

            self.logger.add_in_logs("inf","creating a directory for storing data")
            if(os.path.isdir(self.path + "/Input_files")):
                shutil.rmtree(self.path + "/Input_files")
            
            os.mkdir(self.path + "/Input_files")

            column = open(self.path+"/Source_of_Truth/Data_columns.txt","r")
            input_dataframe = pd.DataFrame(input_data, columns= column.read().split(","))
            input_dataframe.to_csv(self.path + "/Input_files/Input_data.csv", index = False)
            self.logger.add_in_logs("inf", "Exporting to .csv Completed")
            self.logger.add_in_logs("pas","inserting into database process completed")

        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in inserting into table")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def database_package(self):

        """
        This function is main body for the entire class 

        Input : N/A
        Output : Execution of database pipeline
        """
        try:
            self.database_connectivity()
            self.table_creation()
            self.inserting_into_database()  
            self.logger.add_in_logs("END","Database insertion completed successfully")
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in database package")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
