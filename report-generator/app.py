from flask import Flask, render_template, request
import pandas as pd
from prg import webInput, latexCompiler


app = Flask(__name__)
input = webInput.Input() 

@app.route("/")
def main_page():
    return render_template("index.html")
    

@app.route("/customize", methods = ["POST"])
def customize_page():
    f_n = request.files['survey_num']
    f_t = request.files['survey_text']
    input.get_df_n(pd.read_csv(f_n, skiprows=[1, 2])) 
    input.get_df_t(pd.read_csv(f_t, skiprows=[1, 2])) 

    year = input.df_t["Q77#2_1"][2:].dropna().unique()
    year.sort()
    year = [int(i) for i in year]

    gender = input.df_t["Q65"][2:].dropna().unique()
    gender.sort()

    race = input.df_t["Q69"][2:].dropna().unique()
    race_final = []
    for i in race:
        if "," in i:
            race_final = race_final + i.split(",")
        else:
            race_final.append(i)
    race_final = list(set(race_final))
    race_final.sort()

    citizenship = ["US", "International"]

    return render_template("customize.html", year=year, gender=gender, race=race_final, citizenship=citizenship)

@app.route("/generate_report", methods = ['POST'])
def generate_report():
    programs = request.form.getlist("filter1")
    year = request.form.getlist("year")
    gender = request.form.getlist("gender")
    race = request.form.getlist("race")

    citizenship = request.form.getlist("citizenship")
    
    for i in programs:
        compiler = latexCompiler(input.df_n.copy(), input.df_t.copy(), i, gender, race, citizenship, year)
        compiler.generateReport()
    return render_template("final.html")
