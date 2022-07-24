from flask import Flask, render_template, request, send_file
import pandas as pd 
import web_input
from latexCompiler.latexCompiler import latexCompiler


app = Flask(__name__)
input = web_input.Input(None, None, None, None) # better way?

@app.route("/")
def main_page():
    return render_template("index.html")
    

@app.route("/customize", methods = ["POST"])
def customize_page():
    f_n = request.files['survey_num']
    f_t = request.files['survey_text']
    input.get_df_n(pd.read_csv(f_n, skiprows=[1, 2])) 
    input.get_df_t(pd.read_csv(f_t, skiprows=[1, 2])) 

    years = input.df_t["Q77#2_1"][2:].dropna().unique()
    years.sort()
    years = [int(i) for i in years]

    return render_template("customize.html", years = years)

@app.route("/generate_report", methods = ['POST'])
def generate_report():
    programs = request.form.getlist("filter1")
    years = request.form.getlist("year")
    for i in programs:
        compiler = latexCompiler(input.df_n.copy(), input.df_t.copy(), i, years)
        compiler.generateReport()
    return render_template("final.html")
