#------------------------------------------------------------------------------------
# PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
#------------------------------------------------------------------------------------
from pylatex import Document, Section, Figure, Subsection, Command, Itemize, SubFigure, Subsubsection
from pylatex.base_classes.command import Options
from pylatex.utils import italic, NoEscape 
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import math
from .visuals import visuals
# from visuals import visuals

PATH = Path(__file__).resolve().parents[0]
vis = visuals()
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams.update({'font.size': 17})


class latexCompiler:
    
    title_path = PATH.joinpath("def.tex")
    background = "The data that follows was collected via the Exit Survey for Ph.D. Completers. Graduating doctoral students were invited to complete the survey in their final semester in the DEPARTMENT program.  Nineteen of the twenty DEPARTMENT program graduates (95 %) completed the Exit Survey for Ph.D. Completers."

    def filter_program(self, program, program_dict, df_n, df_t):
        df_n_filtered = df_n[df_n["Q1"] == program_dict.get(program)]
        df_t_filtered = df_t[df_t["Q1"] == program]
        return df_n_filtered, df_t_filtered

    def filter_division(self, div, df_n, df_t):
        df_n_filtered = df_n[df_n["Q1"].isin(self.div2program_num.get(div))]
        df_t_filtered = df_t[df_t["Q1"].isin(self.div2program.get(div))]
        return df_n_filtered, df_t_filtered

    def filter_years(self, years, df_n, df_t):
        years_int = [int(i) for i in years]
        df_n_filtered = df_n[df_n["Q77#2_1"].isin(years_int)]
        df_t_filtered = df_t[df_t["Q77#2_1"].isin(years_int)]
        return df_n_filtered, df_t_filtered

    def filter_gender(self, gender, df_n, df_t):
        gender_dict = {"Male": 1, "Female": 2}
        gender_int = [gender_dict[i] for i in gender]
        df_n_filtered = df_n[df_n["Q65"].isin(gender_int)]
        df_t_filtered = df_t[df_t["Q65"].isin(gender)]
        return df_n_filtered, df_t_filtered

    def filter_citizenship(self, citizenship, df_n, df_t):
        df_n_filtered = df_n
        df_t_filtered = df_t

        if "US" not in citizenship:
            df_n_filtered = df_n[df_n["Q67#2_1"].notna()]
            df_t_filtered = df_t[df_t["Q67#2_1"].notna()]

        if "International" not in citizenship:
            df_n_filtered = df_n[df_n["Q67#1_1"].notna()]
            df_t_filtered = df_t[df_t["Q67#1_1"].notna()] 

        return df_n_filtered, df_t_filtered
    
    def sublist(self, lista, listb):
        if isinstance(lista, float):
            return False

        for i in lista:
            if i in listb: return True

        return False

    def filter_race(self, race, df_n, df_t):
        race_dict = {"American Indian or Alaska Native": "1", "Native Hawaiian or other Pacific Islander": "2", "Asian": "3", "African-American/African-Caribbean/Black": "4", "White (non-Hispanic)": "5", "Other": "6"}
        race_int = [race_dict[i] for i in race]
        df_n_filtered = df_n[df_n["Q69"].apply(lambda x: self.sublist(x, race_int))]
        df_t_filtered = df_t[df_t["Q69"].apply(lambda x: self.sublist(x, race))]
        return df_n_filtered, df_t_filtered

    def __init__(self, df_n, df_t, programs, gender, race, citizenship, years, years_str=""):
        self.div2program = {"Humanities": ["Art, Art History and Visual Studies", "German Studies", "Philosophy", "Romance Studies", "Classical Studies", "English", "Literature", "Music", "Religion"], 
    "Biological and Biomedical Sciences": ["Biochemistry", "Biology", "Biostatistics","Cell Biology", "Computational Biology and Bioinformatics", "Ecology", "Evolutionary Anthropology", "Genetics and Genomics", "Immunology", "Medical Physics", "Molecular Cancer Biology", "Molecular Genetics and Microbiology", "Neurobiology", "Pathology", "Pharmacology", "Population Health Sciences"], 
    "Physical Sciences and Engineering": ["Biomedical Engineering", "Chemistry", "Civil and Environmental Engineering", "Computer Science", "Earth and Climate Sciences", "Electrical and Computer Engineering", "Environment", "Marine Science and Conservation", "Mathematics", "Mechanical Engineering and Materials Science", "Physics", "Statistical Science"], 
    "Social Sciences": ["Business Administration", "Cultural Anthropology", "Economics", "Environmental Policy", "History", "Nursing", "Political Science", "Psychology and Neuroscience", "Public Policy Studies", "Sociology"]}
        self.div2program_num = {"Humanities": ["Art, Art History and Visual Studies", "German Studies", "Philosophy", "Romance Studies", "Classical Studies", "English", "Literature", "Music", "Religion"], 
    "Biological and Biomedical Sciences": ["Biochemistry", "Biology", "Biostatistics","Cell Biology", "Computational Biology and Bioinformatics", "Ecology", "Evolutionary Anthropology", "Genetics and Genomics", "Immunology", "Medical Physics", "Molecular Cancer Biology", "Molecular Genetics and Microbiology", "Neurobiology", "Pathology", "Pharmacology", "Population Health Sciences"], 
    "Physical Sciences and Engineering": ["Biomedical Engineering", "Chemistry", "Civil and Environmental Engineering", "Computer Science", "Earth and Climate Sciences", "Electrical and Computer Engineering", "Environment", "Marine Science and Conservation", "Mathematics", "Mechanical Engineering and Materials Science", "Physics", "Statistical Science"], 
    "Social Sciences": ["Business Administration", "Cultural Anthropology", "Economics", "Environmental Policy", "History", "Nursing", "Political Science", "Psychology and Neuroscience", "Public Policy Studies", "Sociology"]}
        self.doc = Document('basic')
        # Raw survey df's
        self.df_n = df_n
        self.df_t = df_t

        self.programs = programs 
        self.years = years 
        self.years_str = years_str
        for y in self.years:
            self.years_str = self.years_str + str(y) + ", "
        self.years_str = self.years_str[:-2]

        # Find numberings for each program 
        keys = df_t["Q1"].tolist()
        values = df_n["Q1"].tolist()
        program_dict = {keys[i]: values[i] for i in range(len(keys))}
        for key in self.div2program_num:
            keys = self.div2program_num.get(key)
            for j in range(len(keys)):
                if keys[j] in program_dict:
                    keys[j] = program_dict.get(keys[j])

        # Fix years for df_n
        self.df_n.dropna(subset=["Q1"], inplace=True)
        self.df_t.dropna(subset=["Q1"], inplace=True)
        self.df_n.loc[:, "Q79#2_1"] = self.df_n["Q79#2_1"] + 1998 # need to fix "before 2011"
        self.df_n.loc[:, "Q77#2_1"] = self.df_n["Q77#2_1"] + 2010
        self.df_n["Q77#2_1"] = self.df_n["Q77#2_1"].fillna(0.0).astype(int)
        self.df_t["Q77#2_1"] = self.df_t["Q77#2_1"].fillna(0.0).astype(int)

        # Fix race for both dfs
        for i in self.df_n["Q69"].index:
            val_n = self.df_n.at[i, "Q69"]
            val_t = self.df_t.at[i, "Q69"]
            if isinstance(val_n, float):
                continue

            if "," in val_n:
                self.df_n.at[i, "Q69"] = val_n.split(",")
                self.df_t.at[i, "Q69"] = (val_t.split(","))
            else:
                self.df_n.at[i, "Q69"] = [val_n]
                self.df_t.at[i, "Q69"] = [val_t]

        # Find division of program
        self.division = ""
        for div in self.div2program:
            if programs in self.div2program.get(div): 
                self.division = div
        self.df_n, self.df_t = self.filter_years(self.years, self.df_n, self.df_t)
        self.df_n, self.df_t = self.filter_gender(gender, self.df_n, self.df_t)
        self.df_n, self.df_t = self.filter_citizenship(citizenship, self.df_n, self.df_t)
        self.df_n, self.df_t = self.filter_race(race, self.df_n, self.df_t)
        self.df_n1, self.df_t1 = self.filter_program(programs, program_dict, df_n, df_t) # This takes a long time... speed up?
        self.df_n2, self.df_t2 = self.filter_division(self.division, df_n, df_t)  

#------------------------------------------------------------------------------------
# DOCUMENT CREATION AND FORMATTING
#------------------------------------------------------------------------------------
    def loadTemplate(self):    
        self.doc.preamble.append(Command("usepackage", "xcolor"))
        self.doc.preamble.append(Command("usepackage", "float"))
        self.doc.preamble.append(Command("include", "def"))
        self.doc.preamble.append(Command("title", "Ph.D. Exit Survey Results"))
        self.doc.preamble.append(Command("author", "Department/Division included in analysis: " + self.programs + "\n" +  "Graduation years included in analysis: " + self.years_str))
        self.doc.preamble.append(Command("date", NoEscape(r"\today")))
        self.doc.append(NoEscape(r'\maketitle'))
        self.doc.append(NoEscape(r'\tableofcontents'))
        self.doc.append(NoEscape(r'\clearpage'))

#------------------------------------------------------------------------------------
# INTRODUCTION
#------------------------------------------------------------------------------------
    def introduction(self, background):
        self.doc.append(NoEscape(r"\clearpage"))
        with self.doc.create(Section("Introduction")):
            self.doc.append(background)
            
            with self.doc.create(Subsection("Summary Statistics")):
                self.doc.append(NoEscape(r'Click \href{https://gradschool.duke.edu/about/program-statistics}{here} for summary data on PhD programs. These data include information such as total applications, admissions, matriculations, demographics, median GRE and GPA scores, and career outcomes.'))
            
            with self.doc.create(Subsection("Overall Assessment")):
                vis.segmented_bar(self.df_n1, [""], ["Q57_4"], ["Definitely, Probably", "Maybe", "Probably not", "Definitely Not"], 2.6)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption('Proportion of students who would recommend the same university to someone considering their field of study.')

                vis.segmented_bar(self.df_n1, ["Academic experience", "Student life experience", "Overall experience"], ["Q54_1", "Q54_2", "Q54_3"], ["Excellent", "Very Good", "Good", "Fair", "Poor"], 8)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Assessment of students' overall satisfaction with three criterions: academic experience, student life experience, and overall experience.")

                with self.doc.create(Figure(position='H')) as plot:
                    self.doc.append(NoEscape(r'\centering'))
                    with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.3\textwidth'))) as subplot1:  
                        scores = [vis.mean_col(self.df_n1, "Q54_1"), vis.mean_col(self.df_n2, "Q54_1")]
                        labels = [self.programs, self.division]
                        vis.single_bar(scores, labels, "", "Score", "Academic experiene", ["#679bc9", "#fdc378"])
                        subplot1.add_plot(width=NoEscape(r'\linewidth'))

                    with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.3\textwidth'))) as subplot2:  
                        scores = [vis.mean_col(self.df_n1, "Q54_2"), vis.mean_col(self.df_n2, "Q54_2")]
                        labels = [self.programs, self.division]
                        vis.single_bar(scores, labels, "", "Score", "Student life experience", ["#679bc9", "#fdc378"])
                        subplot2.add_plot(width=NoEscape(r'\linewidth'))
                    
                    with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.3\textwidth'))) as subplot3:  
                        scores = [vis.mean_col(self.df_n1, "Q54_3"), vis.mean_col(self.df_n2, "Q54_3")]
                        labels = [self.programs, self.division]
                        vis.single_bar(scores, labels, "", "Score", "Overall experience", ["#679bc9", "#fdc378"])
                        subplot3.add_plot(width=NoEscape(r'\linewidth'))
                    
                    plot.add_caption("Average score of student responses in academic experience, student life experience, and overall experience. 5: excellent, 1: poor.")
            plt.close('all')

        
#------------------------------------------------------------------------------------
# TRAINING
#------------------------------------------------------------------------------------
    def training(self):
        self.doc.append(NoEscape(r"\clearpage"))
        with self.doc.create(Section("Training")):
            with self.doc.create(Subsection("Student Perceptions")):
                    questions = ["Q15_" + str(i + 1) for i in range(10)]
                    scores1 = [vis.mean_col(self.df_n1, i) for i in questions]
                    scores2 = [vis.mean_col(self.df_n2, i) for i in questions]
                    labels = ["Intellectual caliber of faculty", "Ability to keep pace w/ field", "Quality of graduate curriculum", "Quality of faculty teaching", "Training in research methods", "Quality of academic advising & guidance", "Preparation for exams", "Opportunity for interdisciplinary work", "Faculty effort in helping find employment", "Overall program quality"] 
                    vis.double_bar(scores1, scores2, labels, self.programs, self.division, "", "Score", "Student Perceptions of Program Quality", 10, 1)
                    with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Average score of student perceptions of program quality where 5 is excellent and 1 is poor")

                    questions = ["Q55_" + str(i + 1) for i in range(5)]
                    scores1 = [vis.mean_col(self.df_n1, i) for i in questions]
                    scores2 = [vis.mean_col(self.df_n2, i) for i in questions]
                    labels = ["Formulate a clear and relevant research question", "Apply appropriate disciplinary research methods", "Analyze data or textual resources critically", "Prepare and offer academic presentations", "Prepare and offer public presentations"]
                    vis.double_bar(scores1, scores2, labels, self.programs, self.division, "", "Score", "Student Perceptions on Training", 10, 1)
                    with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Average score of student perceptions of training where 5 is excellent and 1 is poor")
            
            self.doc.append(NoEscape(r"\clearpage")) #temporary?
            with self.doc.create(Subsection("Presentations and Publications")):
                with self.doc.create(Subsubsection("Presentations")):
                    with self.doc.create(Figure(position='H')) as plot:
                        self.doc.append(NoEscape(r'\centering'))
                        with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.5\textwidth'))) as subplot1:  
                            values1, index1 = vis.df2series(self.df_n1, "Q40") #write function?
                            values1 = vis.fill_zeroes(values1, index1, 11)

                            values2, index2 = vis.df2series(self.df_n2, "Q40")
                            values2 = vis.fill_zeroes(values2, index2, 11)

                            labels = [str(i) for i in range(10)]
                            labels.append("10 or more")

                            vis.double_bar(values1, values2, labels, self.programs, self.division, "Number of scholarly presentations", "Percentage of students", "Scholarly presentations given on campus", 10)
                            subplot1.add_plot(width=NoEscape(r'\linewidth'))

                        with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.5\textwidth'))) as subplot2:  
                            values1, index1 = vis.df2series(self.df_n1, "Q41") #write function?
                            values1 = vis.fill_zeroes(values1, index1, 11)

                            values2, index2 = vis.df2series(self.df_n2, "Q41")
                            values2 = vis.fill_zeroes(values2, index2, 11)

                            labels = [str(i) for i in range(10)]
                            labels.append("10 or more")
                            
                            vis.double_bar(values1, values2, labels, self.programs, self.division, "Number of scholarly presentations", "Percentage of students", "Scholarly presentations away from campus (regional, national, or international)", 10)
                            subplot2.add_plot(width=NoEscape(r'\linewidth'))
                        plot.add_caption("Distribution of number of presentations students gave during their graduate studies on and away from campus")

                    with self.doc.create(Subsubsection("Publications")):
                        with self.doc.create(Figure(position='H')) as plot:
                            self.doc.append(NoEscape(r'\centering'))
                            with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.5\textwidth'))) as subplot1:  
                                values1, index1 = vis.df2series(self.df_n1, "Q44") #write function?
                                values1 = vis.fill_zeroes(values1, index1, 11)

                                values2, index2 = vis.df2series(self.df_n2, "Q44")
                                values2 = vis.fill_zeroes(values2, index2, 11)
                                

                                labels = [str(i) for i in range(10)]
                                labels.append("10 or more")

                                vis.double_bar(values1, values2, labels, self.programs, self.division, "Number of works published or accepted for publication", "Percentage of students", "Published or accepted pblications from graduate research", 10)
                                subplot1.add_plot(width=NoEscape(r'\linewidth'))

                            with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.5\textwidth'))) as subplot2:  
                                values1, index1 = vis.df2series(self.df_n1, "Q45") #write function?
                                values1 = vis.fill_zeroes(values1, index1, 11)

                                values2, index2 = vis.df2series(self.df_n2, "Q45")
                                values2 = vis.fill_zeroes(values2, index2, 11)

                                labels = [str(i) for i in range(10)]
                                labels.append("10 or more")
                                
                                vis.double_bar(values1, values2, labels, self.programs, self.division, "Number of works under review", "Percentage of students", "Number of works under review from graduate research", 10)
                                subplot2.add_plot(width=NoEscape(r'\linewidth'))
                            plot.add_caption("Distribution of number of works that have been published or is under review during graduate reserach")

                            plt.close('all')

#------------------------------------------------------------------------------------
# CAREER PREPARATION AND EMPLOYMENT STATUS AT GRADUATION
#------------------------------------------------------------------------------------
    def career_preparation(self):
        self.doc.append(NoEscape(r"\clearpage"))
        with self.doc.create(Section("Career Preparation and Employment Status at Graduation")):
            with self.doc.create(Subsection("Employment Status")):
                values1, index1 = vis.df2series(self.df_n1, "Q58") 
                values1 = vis.fill_zeroes(values1, index1, 7)

                values2, index2 = vis.df2series(self.df_n2, "Q58")
                values2 = vis.fill_zeroes(values2, index2, 7)

                labels = ["Returning to, or continuing in, pre-doctoral employment", "Having signed contract or made definite commitment for a postdoc or other work", "Negotiating with one or more specific organizations", "Seeking position but have no specific prospects", "Other full-time degree programs (eg MD, DDS, JD)", "Do not plan to work or study (eg family commitmments)", "Other"]
                vis.double_bar(values1, values2, labels, self.programs, self.division, "", "Percentage of students", "Postgraduate plans in the next year", 10, 1)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Distribution of students' postgraduate plans in the next year")

                values1, index1 = vis.df2series(self.df_n1, "Q60") 
                values1 = vis.fill_zeroes(values1, index1, 9)

                values2, index2 = vis.df2series(self.df_n2, "Q60")
                values2 = vis.fill_zeroes(values2, index2, 9)

                labels = ["Postdoctoral researcher or fellow", "Researcher, academic setting", "Researcher, non-academic setting (eg national lab, industry, medical center)", "Tenure track faculty position", "Non-tenure track faculty position", "Academic administration", "Non-academic administration", "Professional or consulting services to individuals", "Other position"]
                vis.double_bar(values1, values2, labels, self.programs, self.division, "", "Percentage of students", "Professional employment type", 10, 1)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Distribution of types of professional employment")

            with self.doc.create(Subsection("Training for Employment")):
                questions = ["Q56#1_" + str(i + 1) for i in range(5)]
                values1 = [vis.prop_col(self.df_n1, i, [1]) for i in questions]
                values2 = [vis.prop_col(self.df_n2, i, [1]) for i in questions]
                labels = ["Writing grant proposal", "Preparing for job interviews", "Preparing a job talk", "Locating positions in academia", "Locating positions outside of academia"]
                vis.double_bar(values1, values2, labels, self.programs, self.division, "", "Percentage of students", "Percentage of students who received training", 10)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Percentage of students who received training in writing grant proposal, preparing for job interviews, preparing a job talk, locating positions in academia, and locating positions outside of academia")

                questions = ["Q56#2_" + str(i + 1) for i in range(5)]
                values1 = [vis.mean_col(self.df_n1, i) for i in questions]
                values2 = [vis.mean_col(self.df_n2, i) for i in questions]
                labels = ["Writing grant proposal", "Preparing for job interviews", "Preparing a job talk", "Locating positions in academia", "Locating positions outside of academia"]
                vis.double_bar(values1, values2, labels, self.programs, self.division, "", "Score", "Student Perceptions of Program Quality", 10)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Average score of student perceptions of training quality where 5 is excellent and 1 is poor")

                values = np.array([])
                for i in range(9):
                    df_temp = vis.filter_value(self.df_n2, "Q60", [i+1])
                    questions = ["Q56#1_" + str(i + 1) for i in range(5)]
                    temp = [vis.mean_col(df_temp, q, 5) for q in questions]
                    values = np.append(values, np.array(temp))
                
                values = np.transpose(values.reshape(9, 5))
                label1 = ["Postdoctoral researcher or fellow", "Researcher, academic setting", "Researcher, non-academic setting (eg national lab, industry, medical center)", "Tenure track faculty position", "Non-tenure track faculty position", "Academic administration", "Non-academic administration", "Professional or consulting services to individuals", "Other position"]
                label2 = ["Writing grant proposal", "Preparing for job interviews", "Preparing a job talk", "Locating positions in academia", "Locating positions outside of academia"]
                vis.heatmap_final(values, label1, label2, "Average score of each training type for various professional employments for " + self.division, "Score")
                
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Average score of each training type for students of various professional employments where 4: Very satisfied and 1: Very dissatisfied for " + self.division)

                plt.close('all')
            # Advisor's help in finding employment...

#------------------------------------------------------------------------------------
# MENTORING, ADVISING, AND PROGRAM CLIMATE
#------------------------------------------------------------------------------------
    def advising(self):
        self.doc.append(NoEscape(r"\clearpage"))
        with self.doc.create(Section("Mentoring, Advising, and Program Climate")):
            with self.doc.create(Subsection("Overall Assessment")):
                with self.doc.create(Figure(position='H')) as plot:
                    self.doc.append(NoEscape(r'\centering'))
                    with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.5\textwidth'))) as subplot1:  
                        scores = [vis.mean_col(self.df_n1, "Q15_6"), vis.mean_col(self.df_n2, "Q15_6")]
                        labels = [self.programs, self.division]
                        vis.single_bar(scores, labels, "", "Score", "Academic advising quality", ["#679bc9", "#fdc378"])
                        subplot1.add_plot(width=NoEscape(r'\linewidth'))
                        subplot1.add_caption("Average score where 5 is excellent and 1 is poor")

                    with self.doc.create(SubFigure(position='b', width=NoEscape(r'0.5\textwidth'))) as subplot2:  
                        scores = [vis.mean_col(self.df_n1, "Q57_3"), vis.mean_col(self.df_n2, "Q57_3")]
                        labels = [self.programs, self.division]
                        vis.single_bar(scores, labels, "", "Score", "Would you select the same dissertation advisor?",  ["#679bc9", "#fdc378"])
                        subplot2.add_plot(width=NoEscape(r'\linewidth'))
                        subplot2.add_caption("Average score where 5 is detinitely and 1 is definitely not")
            with self.doc.create(Subsection("Dissertation Advisor and Perception of Program Quality")):
                    df_temp = vis.filter_value(self.df_n2, "Q57_3", [1, 2, 3])
                    questions = ["Q15_" + str(i + 1) for i in range(10)]
                    values1 = [vis.mean_col(df_temp, q) for q in questions]
                    questions = ["Q16_" + str(i + 1) for i in range(9)]
                    values3 = [vis.mean_col(df_temp, q) for q in questions]
                    df_temp = vis.filter_value(self.df_n2, "Q57_3", [4, 5])
                    questions = ["Q15_" + str(i + 1) for i in range(10)]
                    values2 = [vis.mean_col(df_temp, q) for q in questions]   
                    questions = ["Q16_" + str(i + 1) for i in range(9)]
                    values4 = [vis.mean_col(df_temp, q) for q in questions]   
                    labels = ["Intellectual caliber of faculty", "Ability to keep pace w/ field", "Quality of graduate curriculum", "Quality of faculty teaching", "Training in research methods", "Quality of academic advising & guidance", "Preparation for exams", "Opportunity for interdisciplinary work", "Faculty effort in helping find employment", "Overall program quality"] 
                    vis.double_bar(values1, values2, labels, "Probably or definitely would select same dissertation advisor", "Maybe, probably not, or definitely not select same dissertation advisor", "", "Score", "Program quality scores by willingness to select the same dissertation advisor again", 10, 1)
                    
                    with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Average scores of training program and program quality between students likely and unlikely to select the same dissertation advisor again where 5 is excellent and 1 is poor")
            with self.doc.create(Subsection("Dissertation Advisor and Program Climate")):
                labels = ["Faculty treat students w/ respect", "Intellectual climate is positive", "Social climate is positive", "Students are collegial", "Staff members are helpful", "Tensions among faculty that affect students", "Financial support is distributed fairly", "Advisor served as advocate when necessary", "Faculty support multiple career paths"] 
                vis.double_bar(values3, values4, labels, "Probably or definitely would select same dissertation advisor", "Maybe, probably not, or definitely not select same dissertation advisor", "", "Score", "Program climate scores by willingness to select same advisor again", 10, 1)
                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'1\textwidth'))
                    plot.add_caption("Average scores of climate of program and obstacles to success between students likely and unlikely to select the same dissertation advisor again where 5 is excellent and 1 is poor")

            with self.doc.create(Subsection("Identifying Important Factors in Advising")):
                    questions = ["Q23#1_" + str(i + 1) for i in range(9)]
                    questions.append("Q57_3")
                    temp = self.df_n1[questions].dropna()

                    mean = []
                    corr = []
                    labels = ["Preparing for written qualifying exams", "Preparing for the oral qualifying exam", "Selecting a dissertation topic", "Writing a disseration on prospectus or proposal", "Doing research for dissertation", "Writing and revising disseration", "Identifying academic career options", "Identifying non-academic career options", "Searching for employment or training"]
                    for i in range(len(questions) - 1):
                        mean.append(vis.mean_col(self.df_n1, questions[i]))
                        corr.append(vis.spearman_corr(temp[questions[i]], temp["Q23#1_1"])[0])
                    vis.scatter(mean, corr, labels, "mean", "R", "Correlation between factors of advising and average scores of whether students would select dissertation advisor again", 8)
                    with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Correlation between factors of advising and average scores of whether students would select dissertation advisor again. Top right means important and doing well. Top left means important but doing poorly. Bottom right means unimportant but doing well. Bottom left means unimportant and doing bad.")
                            
                    
            with self.doc.create(Subsection("Additional Faculty Mentors")):
                labels = ["yes", "no"]
                yes_prop = vis.prop_col(self.df_n1, "Q24", [1])
                dept_prop = vis.prop_col(self.df_n1, "Q25", [1])
                i1 = yes_prop / 100 * dept_prop
                values1 = [i1, 100 - yes_prop]
                values2 = [yes_prop - i1, 0]
                fig, ax = plt.subplots()
                ax.bar(labels, values1, color="#679bc9")
                ax.bar(labels, values2, bottom=values1, color="#fdc378")
                ax.set_xlabel("")
                ax.set_ylabel("Percentage of students")
                ax.legend(["Within Department", "Outside Department"])
                ax.set_title("Students with additional faculty mentors")

                with self.doc.create(Figure(position='H')) as plot:
                    plot.add_plot(width=NoEscape(r'0.6\textwidth'))
                    plot.add_caption("Percentage of students with additional faculty mentors, and percentage of which mentors were within the same department")
 
                with self.doc.create(Subsubsection("Additional Mentorship and Perceptions of Program Quality")):
                    df_temp = vis.filter_value(self.df_n2, "Q24", [1])
                    questions = ["Q15_" + str(i + 1) for i in range(10)]
                    values1 = [vis.mean_col(df_temp, q) for q in questions]
                    questions = ["Q16_" + str(i + 1) for i in range(9)]
                    values3 = [vis.mean_col(df_temp, q) for q in questions]
                    df_temp = vis.filter_value(self.df_n2, "Q24", [2])
                    questions = ["Q15_" + str(i + 1) for i in range(10)]
                    values2 = [vis.mean_col(df_temp, q) for q in questions]   
                    questions = ["Q16_" + str(i + 1) for i in range(9)]
                    values4 = [vis.mean_col(df_temp, q) for q in questions]   
                    labels = ["Intellectual caliber of faculty", "Ability to keep pace w/ field", "Quality of graduate curriculum", "Quality of faculty teaching", "Training in research methods", "Quality of academic advising & guidance", "Preparation for exams", "Opportunity for interdisciplinary work", "Faculty effort in helping find employment", "Overall program quality"] 
                    vis.double_bar(values1, values2, labels, "Additional faculty mentor", "No additional faculty mentor", "", "Score", "Program quality averages by additional faculty mentor status", 10, 1)

                    
                    with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Average scores of training program and program quality between students likely and unlikely to select the same dissertation advisor again where 5 is excellent and 1 is poor")
                with self.doc.create(Subsubsection("Additional Mentorship and Program Climate")):
                    labels = ["Faculty treat students w/ respect", "Intellectual climate is positive", "Social climate is positive", "Students are collegial", "Staff members are helpful", "Tensions among faculty that affect students", "Financial support is distributed fairly", "Advisor served as advocate when necessary", "Faculty support multiple career paths"] 
                    vis.double_bar(values3, values4, labels, "Additional faculty mentor", "No additional faculty mentor", "", "Score", "Program climate averages by additional faculty mentor status", 10, 1)
                    with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Average scores of climate of program and obstacles to success between students likely and unlikely to select the same dissertation advisor again where 5 is excellent and 1 is poor")
           
            with self.doc.create(Subsection("Program Climate in Division")):
                questions = ["Q16_" + str(i + 1) for i in range(9)]
                values1 = [vis.mean_col(self.df_n1, i) for i in questions]
                values2 = [vis.mean_col(self.df_n2, i) for i in questions]
                labels = ["Faculty treat students w/ respect", "Intellectual climate is positive", "Social climate is positive", "Students are collegial", "Staff members are helpful", "Tensions among faculty that affect students", "Financial support is distributed fairly", "Advisor served as advocate when necessary", "Faculty support multiple career paths"]  
                vis.double_bar(values1, values2, labels, self.programs, self.division, "", "Score", "Comparing program climate with division climate", 10, 1)
                with self.doc.create(Figure(position='H')) as plot:
                        plot.add_plot(width=NoEscape(r'1\textwidth'))
                        plot.add_caption("Comparing department climate with division climate")

            plt.close('all')
#------------------------------------------------------------------------------------
# FREE RESPONSE QUESTIONS
#------------------------------------------------------------------------------------
    def frq(self):
        self.doc.append(NoEscape(r"\clearpage"))
        with self.doc.create(Section("Free Response Questions")):
            self.doc.append("TODO")

#------------------------------------------------------------------------------------
# ADDITIONAL INSIGHTS
#------------------------------------------------------------------------------------
    def addtl(self):
        self.doc.append(NoEscape(r"\clearpage"))
        with self.doc.create(Section("Additional Insights")):
            self.doc.append("TODO")

#------------------------------------------------------------------------------------
# GENERATE DOCUMENT
#------------------------------------------------------------------------------------
    FINAL_PATH = Path(__file__).resolve().parents[2]
    
   
    def generateDoc(self):
        filepath = self.FINAL_PATH.joinpath("reports/" + "-".join(self.division.lower().split(" "))+ "/final-report-" + "-".join(self.programs.lower().split(" ")))
        self.doc.generate_pdf(filepath, compiler="xelatex", clean=False, clean_tex=False)
        self.doc.generate_pdf(filepath, compiler="xelatex", clean = True, clean_tex = True)
        
    def generateReport(self):
        self.loadTemplate()
        self.introduction(self.background)
        self.training()
        self.career_preparation()
        self.advising()
        self.frq()
        self.addtl()
        self.generateDoc()
    

if __name__ == "__main__":
    df_n = pd.read_csv("/Users/stan.park712/Desktop/exit-survey-numeric.csv", skiprows=[1, 2])
    df_t = pd.read_csv("/Users/stan.park712/Desktop/exit-survey-text.csv", skiprows=[1, 2])
    compiler = latexCompiler(df_n, df_t, "Biology", ["2016", "2017"])
    compiler.listCheck(["1", "2", "3"], df_n["Q69"])
        
    # df_n["Q69"].iloc[37] = ["1", "3"]
    # compiler = latexCompiler(df_v, df_t, "Biology", ["2016", "2017"])
    # print(compiler.FINAL_PATH)
    # compiler.generateReport()