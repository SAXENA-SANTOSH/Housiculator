"""
This is the main  python file which is used to connect front end and back end.
Each and every features and module is routed to this application

Developed by Santosh Saxena
on 23/4/2021
"""
#Module Declaration
#-----------------------------------------------------------------------#
import os
import sys
import shutil
import pickle
import numpy as np
import pandas as pd
import plotly.express as ex
from training import Training
import plotly.graph_objects as go
from Prediction.prediction import Prediction
from Logger.runtime_logger import Runtime_Logger
from flask import Flask , render_template , request , jsonify , url_for 
#-----------------------------------------------------------------------#

try:
    path = str(os.getcwd())
    data_base_name = "House"
    data_base_table_name = "House_table"

    app = Flask(__name__)

    run_time_logger = Runtime_Logger(path)

# Home Page
    @app.route("/", methods = ["GET","POST"])
    def home_page():
        try:
            run_time_logger.add_in_logs("Started Model Training")
            global overall_accuracy
            overall_accuracy = Training().train(path , data_base_name , data_base_table_name)
            overall_accuracy = round(overall_accuracy , 2)
            run_time_logger.add_in_logs("Log in to application")
            return render_template("home_page.html")
        except:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "Home Page module")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e) )
    
# Problem Statement
    @app.route("/problem_statement" , methods = [ "GET" ,"POST" ])
    def problem_statement():
        try:
            run_time_logger.add_in_logs("Viewed Porblem Statement")
            problem_file = open(path + "/Source_of_Truth/Problem_Satement.txt","r")
            data_file = open(path + "/Source_of_Truth/data_description.txt", "r")
            return render_template("problem_statement.html" , problem_statement = problem_file.read(), data_description = data_file.read() )
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("Problem Statement module")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))


# generated logs Logs
    @app.route("/logs" , methods = ["GET" , "POST"])
    def logs():
        try:
            run_time_logger.add_in_logs("Viewed Machine Activities of training")
            log_file = open(path + "/Logger/Log_file.txt","r")
            meta_data = open(path + "/Logger/Log_file_metadata.txt","r")
            return render_template("ai_model_activity.html" ,logs = log_file.read(), meta_data = meta_data.read())
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("AI model activity")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# Dataset 

    @app.route("/dataset" , methods = ["GET" , "POST"])
    def dataset():
        try:
            good_dataset = open(path + "/Model_files/good_data.txt","w")
            good_dataset.write("\n")
            for i in os.listdir(path + "/Good_Dataset"):
                good_dataset.write(str(i))
                good_dataset.write("\n")
            good_dataset.close()
            bad_dataset = open(path + "/Model_files/bad_data.txt","w")
            bad_dataset.write("\n")
            for i in os.listdir(path + "/Bad_Dataset"):
                bad_dataset.write(str(i))
                bad_dataset.write("\n")
                print(i)
            bad_dataset.close() 

            good_dataset = open(path + "/Model_files/good_data.txt" , "r")
            bad_dataset = open(path + "/Model_files/bad_data.txt" , "r")
        
            return render_template("dataset.html"  , good_data = str(good_dataset.read()) , bad_data = str(bad_dataset.read()))
       
        except Exception as e:
            run_time_logger.add_in_logs( "Training module")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# EDA

    @app.route("/eda" , methods = ["GET" , "POST"])
    def eda():
        try:
            run_time_logger.add_in_logs("Viewed EDA")
            eda_reader = open(path + "/EDA/Metadata.txt","r")
            return render_template("eda.html" , eda = eda_reader.read() )
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("eda")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# AI Model training

    @app.route("/Training" , methods = ["GET" , "POST"])
    def training():
        try:
            run_time_logger.add_in_logs("Started Model Training")
            global overall_accuracy
            overall_accuracy = Training().train(path , data_base_name , data_base_table_name)
            overall_accuracy = round(overall_accuracy , 2)
            return render_template("done.html" , text = "Training completed successfully")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "Training")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs((str(e)))
            return render_template("error.html"  , text = str(e))

# generated plots homepage 

    @app.route("/plots_home_page" , methods = ["GET" , "POST"])
    def plot():
        try:
            run_time_logger.add_in_logs("Viewing plots generated while training")
            return render_template("generating_plots.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "plots home page")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
    
# Generated plots pie plot

    @app.route("/pie" , methods = ["GET" , "POST"])
    def pie_plot():
        try:
            run_time_logger.add_in_logs("Viewing pie plots generated while training")
            return render_template("plots/pie.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "Pie plot")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# generated plot bar plot

    @app.route("/bar" , methods = ["GET" , "POST"])
    def bar_plot():
        try:
            run_time_logger.add_in_logs("Viewing bar plot generated while training")
            return render_template("plots/bar.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "Bar Plot")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# generated plot distribution plot

    @app.route("/distribution" , methods = ["GET" , "POST"])
    def distribution_plot():
        try:
            run_time_logger.add_in_logs("Viewing distributed plots generated while training")
            return render_template("plots/distribution.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an Error")
            run_time_logger.add_in_logs( "distribution")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# generated plot box plot

    @app.route("/box" , methods = ["GET" , "POST"])
    def box_plot():
        try:
            run_time_logger.add_in_logs("Viewing box plot generatedd while training")
            return render_template("plots/box.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "Box plot")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# generated plot scatter

    @app.route("/scatter" , methods = ["GET" , "POST"])
    def scatter_plot():
        try:
            run_time_logger.add_in_logs("Viewing scatter plots generated while training")
            return render_template("plots/scatter.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "scatter")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# generated plot ai model

    @app.route("/ai_model_plot" , methods = ["GET" , "POST"])
    def ai_model():
        try:
            run_time_logger.add_in_logs("Viewed AI related plots")
            return render_template("plots/ai_model.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "ai model plot")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))


    @app.route("/custom" , methods = ["GET" , "POST"])
    def custom():
        try:
            run_time_logger.add_in_logs("visited advanced plots home page")
            return render_template("generating_custom_plots.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "custom plot")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
    
    @app.route("/categorical_1d_homepage" , methods = ["GET" , "POST"])
    def pie_custom():
        try:
            run_time_logger.add_in_logs("visited 1d categorical advanced plot")
            return render_template("Custom_plots/categorical_1d.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "categorical 1d")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
    
    @app.route("/continuous_1d_homepage" , methods = ["GET" , "POST"])
    def continuous_1d_homepage():
        try:
            run_time_logger.add_in_logs("visited continuous 1d advanced plot")
            return render_template("Custom_plots/continuous_1d.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "continuous 1d")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
    
    
    @app.route("/plots_2d_homepage" , methods = ["GET" , "POST"])
    def plots_2d_homepage():
        try:
            run_time_logger.add_in_logs("visited 2d advanced plots ")
            return render_template("Custom_plots/plot_2d.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "2d plots")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
        

    @app.route("/plots_3d_homepage" , methods = ["GET" , "POST"])
    def plots_3d_homepage():
        try:
            run_time_logger.add_in_logs("Visited 3d advanced plots")
            return render_template("Custom_plots/plot_3d.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "3d plots")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/continuous_3d_homepage" , methods = ["GET" , "POST"])
    def continuous_3d_homepage():
        try:
            run_time_logger.add_in_logs("Visited 3d continuous advanced plots")
            return render_template("Custom_plots/continuous_3d.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "3d continuous plots")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
    


    @app.route("/categorical_1d" , methods = ["POST"])
    def categorical_1d():
        try:
            run_time_logger.add_in_logs("Used 1d categorical advanced plots")
            if(request.method == "POST"):
                x = str(request.form["x_axis"])
                plot = str(request.form["type"])
                
                df = pd.read_csv(path +"/Input_files/Dataset.csv")

                if(plot == "pie"):
                    fig = ex.pie(data_frame=df , names=  x)
                if(plot == "violin"):
                    fig = ex.violin(data_frame=df , x = x)
                if(plot == "bar"):
                    score = []
                    for j in pd.Categorical(df[x]).categories:
                        score.append((df[x] == j).sum())
                    fig = ex.bar(data_frame=df , x = pd.Categorical(df[x]).categories , y = score)

                fig.write_html(path + "/templates/advance_plot.html")
                return render_template("advance_plot.html")

            else:
                raise("error in method")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "1d categorical input")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/continuous_1d" , methods = ["POST"])
    def continuous_1d():
        try:
            run_time_logger.add_in_logs("used 1d continuous advanced plots")
            if(request.method == "POST"):
                x = str(request.form["x_axis"])
                label = str(request.form["label"])
                plot = str(request.form["type"])
                
                df = pd.read_csv(path +"/Input_files/Dataset.csv")

                if(plot == "box"):
                    fig = ex.box(data_frame=df , x= x , color = label)
                if(plot == "histogram"):
                    fig = ex.histogram(data_frame= df , x = x , color=label , marginal="box")
                fig.write_html(path + "/templates/advance_plot.html")
                return render_template("advance_plot.html")

            else:
                raise("error in method")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("1d continuous input")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/plot_2d" , methods = ["POST"])
    def plot_2d():
        try:
            run_time_logger.add_in_logs("Used 2d advanced plots")
            if(request.method == "POST"):
                x = str(request.form["x_axis"])
                y = str(request.form["y_axis"])
                label = str(request.form["label"])

                
                df = pd.read_csv(path +"/Input_files/Dataset.csv")

                
                fig = ex.scatter(data_frame= df , x = x, y = y , color=label , marginal_x= "histogram" , marginal_y="box")
                
                fig.write_html(path + "/templates/advance_plot.html")
                return render_template("advance_plot.html")
            else:
                raise("error in method")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("2d plots")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/plot_3d" , methods = ["POST"])
    def plot_3d():
        try:
            run_time_logger.add_in_logs("used 3d advanced plots")
            if(request.method == "POST"):
                x = str(request.form["x_axis"])
                y = str(request.form["y_axis"])
                z = str(request.form["z_axis"])
                label = str(request.form["label"])
                plot = str(request.form["type"])
                
                df = pd.read_csv(path +"/Input_files/Dataset.csv")

                if(plot == "scatter"):
                    fig = ex.scatter_3d(data_frame=df , x = x , y = y , z = z , color = label)
                run_time_logger.add_in_logs(label)

                fig.write_html(path + "/templates/advance_plot.html")
                return render_template("advance_plot.html")

            else:
                raise("error in method")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("3d plot")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))


    @app.route("/continuous_3d" , methods = ["POST"])
    def continuous_3d():
        try:
            run_time_logger.add_in_logs("used 3d continuous advanced plots")
            if(request.method == "POST"):
                x = str(request.form["x_axis"])
                y = str(request.form["y_axis"])
                z = str(request.form["z_axis"])
                plot = str(request.form["type"])
            
                df = pd.read_csv(path +"/Input_files/Dataset.csv")

                if(plot == "mesh"):
                    fig = go.Figure(data=[go.Mesh3d(x = df[x] , y = df[y] , z = df[z])])
                    fig.update_layout(scene = dict(
                    xaxis_title= x,
                    yaxis_title= y,
                    zaxis_title= z ))
                if(plot == "surface"):
                    fig = go.Figure(data=[go.Surface(z=df[[x,y,z]].values)])
                    fig.update_layout(scene = dict(
                    xaxis_title= x,
                    yaxis_title= y ,
                    zaxis_title= z ))
                
                fig.write_html(path + "/templates/advance_plot.html")
                return render_template("advance_plot.html")
        
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("3d continuous")
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# Accuracy

    @app.route("/accuracy" , methods = ["GET" , "POST"])
    def accuracy():
        try:
            run_time_logger.add_in_logs("Checked the accuracy")
            file = open(path + "/static/accuracy.txt" , "r")
            return render_template("accuracy.html" , accuracy_text = file.read() , overall_accuracy = overall_accuracy)
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "eda")
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

# Add dataset

    @app.route("/add_data_homepage" , methods = ["GET" , "POST"])
    def add_data_homepage():
        try:
            run_time_logger.add_in_logs("Adding external data")
            return render_template("/add_dataset.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "add data homepage")
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/add_dataset" , methods = ["POST"])
    def add_dataset():
        try:
            run_time_logger.add_in_logs("Added external data")
            if(request.method == "POST"):
                target_path = str(request.form["file_path"])
                if(os.path.isfile(target_path)):
                    shutil.copy(target_path , path + "/Training_Batch_Folder")
            return render_template("done.html"  , text  = "Data is added successfully ")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "add dataset")
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))
        
    @app.route("/history" , methods = ["GET" , "POST"])
    def history():
        try:
            run_time_logger.add_in_logs("Watched History")
            log_file = open(path + "/Logger/runtime_Log_file.txt" , "r")
            return render_template("history.html" , data = str(log_file.read()))
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "history")
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/prediction" , methods = ["GET" , "POST"])
    def prediction():
        try:
            run_time_logger.add_in_logs("Visiting Prediction features")
            return render_template("/prediction.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs( "add data homepage")
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html"  , text = str(e))

    @app.route("/prediction_file" , methods = ["POST"])
    def prediction_input():
        try:
            run_time_logger.add_in_logs("Using Prediction features")
            if(request.method == "POST"):
                target_path = str(request.form["prediction_file"])
            p = Prediction(path , target_path , run_time_logger)
            p.prediction_package()
            if(p.condition):
                text = "Prediction done successfully"
            else:
                text = "Data has not satisfied the requireed conditions"
            
            return render_template("done.html"  , text =text)
        
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("Prediction")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html", text = str(e))

    @app.route("/view" , methods = ["GET" , "POST"])
    def view():
        try:
            run_time_logger.add_in_logs("Visting view prediction")
            return render_template("view.html")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("view prediction home page")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html", text = str(e))
    
    @app.route("/view_predictions" , methods = ["POST"])
    def view_prediction():
        try:
            run_time_logger.add_in_logs("Using view prediction")
            if(request.method == "POST"):
                target_path = request.form["file_path"]
            if(os.path.isfile(path + "/Prediction/Predicted_Data/" + str(target_path))):
                df = pd.read_csv(path + "/Prediction/Predicted_Data/" + str(target_path))
                df.to_html(path + "/templates/prediction_file.html")
                return render_template("prediction_file.html")
            else:
                return render_template("error.html" , text = "file name is not correct or you havent predicted this file using AI model prediction")
        except Exception as e:
            run_time_logger.add_in_logs("Faced an error")
            run_time_logger.add_in_logs("view prediction")
            run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            run_time_logger.add_in_logs(str(e))
            return render_template("error.html", text = str(e))





    


    if __name__ == "__main__":
        app.run(debug=True)

except Exception as e:
    run_time_logger.add_in_logs("Faced an error")
    run_time_logger.add_in_logs( "Main application")
    run_time_logger.add_in_logs("Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
    run_time_logger.add_in_logs(str(e))




except Exception as e:
    run_time_logger.add_in_logs("Main")