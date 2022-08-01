import pandas as pd 
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import math
import scipy.stats

class visuals():
    def fill_zeroes(self, values, index, num):
        for i in range(num): 
            if not i+1 in index:
                values.insert(i, 0)
        return values

    def df2series(self, df, question):
        col = df[question].dropna().astype(int)
        series = col.value_counts(normalize=True, sort=False).sort_index()
        temp = series.to_list()
        values = [round(x * 100, 2) for x in temp]
        labels = series.index.tolist()
        return values, labels  

    def segmented_bar(self, df, labels, questions, category_names, ht):
        qs = ["Q54_1", "Q54_2", "Q54_3"]
        results = {}
        category_names = ["Excellent", "Very Good", "Good", "Fair", "Poor"]

        for q in questions:
            val, lab = self.df2series(df, q)
            val = self.fill_zeroes(val, lab, 5)
            results[q] = val

        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.colormaps['RdYlBu'](
            np.linspace(0.15, 0.85, data.shape[1]))
        category_colors = category_colors[::-1]

        fig, ax = plt.subplots(figsize=(20, ht))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.8,
                            label=colname, color=color)

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            ax.bar_label(rects, label_type='center', color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='medium')

        # fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        # plt.show()

    def mean_col(self, df, question, score=6):
        values = df[question].dropna()
        if values.empty:
            return math.nan
        values = [score - i for i in values]
        return round(sum(values) / len(values), 2) # Incorporate confidence intervals 

    def prop_col(self, df, question, target):
        col = df[question].dropna()
        series = col.value_counts(normalize=True, sort=False).sort_index()
        index = series.index.tolist()
        temp = series.to_list()
        values = [round(x * 100, 2) for x in temp]

        percentage = 0
        for i in range(len(index)):
            if index[i] in target:
                percentage = percentage + values[i]
        
        return percentage



    def filter_value(self, df, question, value):
        return df.loc[df[question].isin(value)] 

    def single_bar(self, values, labels, xlabel, ylabel, title, color=["#679bc9"]): # make arguments optional?
       fig, ax = plt.subplots()
       bar1 = ax.bar(labels, values, color=color)

       ax.set_xlabel(xlabel)
       ax.set_ylabel(ylabel)
       ax.set_title(title)
       ax.bar_label(bar1)

    def double_bar(self, values1, values2, labels, lab1, lab2, xlabel, ylabel, title, ht, rotate=0, color1=["#679bc9"], color2=["#fdc378"]):
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots(figsize=(25, ht))
        bar1 = ax.bar(x - width/2, values1, width, label=lab1, color=color1)
        bar2 = ax.bar(x + width/2, values2, width, label=lab2, color=color2)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(x, labels)
        ax.legend()
        ax.bar_label(bar1)
        ax.bar_label(bar2)
        if rotate == 1:
            fig.autofmt_xdate(rotation=37)
        plt.tight_layout()
        # plt.show()

    def heatmap(self, data, row_labels, col_labels, ax=None,
                cbar_kw={}, cbarlabel="", **kwargs):

        if not ax:
            ax = plt.gca()

        # Plot the heatmap
        im = ax.imshow(data, **kwargs)

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

        # Show all ticks and label them with the respective list entries.
        ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
        ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=False, bottom=True,
                    labeltop=False, labelbottom=True)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right",
                rotation_mode="anchor")

        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)

        ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        return im, cbar


    def annotate_heatmap(self, im, data=None, valfmt="{x:.2f}",
                        textcolors=("black", "white"),
                        threshold=None, **textkw):

        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

        # Normalize the threshold to the images color range.
        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max())/2.

        # Set default alignment to center, but allow it to be
        # overwritten by textkw.
        kw = dict(horizontalalignment="center",
                verticalalignment="center")
        kw.update(textkw)

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)

        return texts

    def heatmap_final(self, values, label1, label2, title, metric, ht=10, xlabel="", ylabel=""):
        fig, ax = plt.subplots(figsize=(15, ht))

        im, cbar = self.heatmap(values, label2, label1, ax=ax,
                        cmap="Blues", cbarlabel=metric)
        texts = self.annotate_heatmap(im, valfmt="{x:.1f}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        plt.tight_layout()

    def spearman_corr(self, q1, q2):
        return scipy.stats.spearmanr(q1, q2)

    def scatter(self, x, y, labels, xlabel, ylabel, title, ht=10):
        fig, ax = plt.subplots(figsize=(15, ht))
        for i in range(len(x)):
            ax.scatter(x[i], y[i])
            ax.annotate(labels[i], (x[i], y[i]))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        plt.tight_layout()


if __name__ == "__main__":

    def filter_program(program, program_dict, df_n, df_t):
        df_n_filtered = df_n[df_n["Q1"] == program_dict.get(program)]
        df_t_filtered = df_t[df_t["Q1"] == program]
        return df_n_filtered, df_t_filtered

    def filter_division(div, df_n, df_t):
        df_n_filtered = df_n[df_n["Q1"].isin(div2program_num.get(div))]
        df_t_filtered = df_t[df_t["Q1"].isin(div2program.get(div))]
        return df_n_filtered, df_t_filtered

    df_n = pd.read_csv("/Users/stan.park712/Desktop/exit-survey-numeric.csv", skiprows=[1, 2])
    df_t = pd.read_csv("/Users/stan.park712/Desktop/exit-survey-text.csv", skiprows=[1, 2])

    div2program = {"Humanities": ["Art, Art History and Visual Studies", "German Studies", "Philosophy", "Romance Studies", "Classical Studies", "English", "Literature", "Music", "Religion"], 
"Biological and Biomedical Sciences": ["Biochemistry", "Biology", "Biostatistics","Cell Biology", "Computational Biology and Bioinformatics", "Ecology", "Evolutionary Anthropology", "Genetics and Genomics", "Immunology", "Medical Physics", "Molecular Cancer Biology", "Molecular Genetics and Microbiology", "Neurobiology", "Pathology", "Pharmacology", "Population Health Sciences"], 
"Physical Sciences and Engineering": ["Biomedical Engineering", "Chemistry", "Civil and Environmental Engineering", "Computer Science", "Earth and Climate Sciences", "Electrical and Computer Engineering", "Environment", "Marine Science and Conservation", "Mathematics", "Mechanical Engineering and Materials Science", "Physics", "Statistical Science"], 
"Social Sciences": ["Business Administration", "Cultural Anthropology", "Economics", "Environmental Policy", "History", "Nursing", "Political Science", "Psychology and Neuroscience", "Public Policy Studies", "Sociology"]}
    div2program_num = {"Humanities": ["Art, Art History and Visual Studies", "German Studies", "Philosophy", "Romance Studies", "Classical Studies", "English", "Literature", "Music", "Religion"], 
"Biological and Biomedical Sciences": ["Biochemistry", "Biology", "Biostatistics","Cell Biology", "Computational Biology and Bioinformatics", "Ecology", "Evolutionary Anthropology", "Genetics and Genomics", "Immunology", "Medical Physics", "Molecular Cancer Biology", "Molecular Genetics and Microbiology", "Neurobiology", "Pathology", "Pharmacology", "Population Health Sciences"], 
"Physical Sciences and Engineering": ["Biomedical Engineering", "Chemistry", "Civil and Environmental Engineering", "Computer Science", "Earth and Climate Sciences", "Electrical and Computer Engineering", "Environment", "Marine Science and Conservation", "Mathematics", "Mechanical Engineering and Materials Science", "Physics", "Statistical Science"], 
"Social Sciences": ["Business Administration", "Cultural Anthropology", "Economics", "Environmental Policy", "History", "Nursing", "Political Science", "Psychology and Neuroscience", "Public Policy Studies", "Sociology"]}

    # Find numberings for each program 
    keys = df_t["Q1"].tolist()
    values = df_n["Q1"].tolist()
    program_dict = {keys[i]: values[i] for i in range(len(keys))}
    for key in div2program_num:
        keys = div2program_num.get(key)
        for j in range(len(keys)):
            if keys[j] in program_dict:
                keys[j] = program_dict.get(keys[j])

    # Fix years for df_n
    df_n.dropna(subset=["Q1"], inplace=True)
    df_n.loc[:, "Q79#2_1"] = df_n["Q79#2_1"] + 1998 # need to fix "before 2011"
    df_n.loc[:, "Q77#2_1"] = df_n["Q77#2_1"] + 2010

    programs = "Biology"
    # Find division of program
    division = ""
    for div in div2program:
        if programs in div2program.get(div): 
            division = div

    df_n1, df_t1 = filter_program(programs, program_dict, df_n, df_t) # This takes a long time... speed up?
    df_n2, df_t2 = filter_division(division, df_n, df_t)   

    vis = visuals()
    questions = ["Q23#1_" + str(i + 1) for i in range(9)]
    questions.append("Q57_3")
    temp = df_n1[questions].dropna()

    mean = []
    corr = []
    labels = ["Preparing for written qualifying exams", "Preparing for the oral qualifying exam", "Selecting a dissertation topic", "Writing a disseration on prospectus or proposal", "Doing research for dissertation", "Writing and revising disseration", "Identifying academic career options", "Identifying non-academic career options", "Searching for employment or training"]
    for i in range(len(questions) - 1):
        mean.append(vis.mean_col(df_n1, questions[i]))
        corr.append(vis.spearman_corr(temp[questions[i]], temp["Q23#1_1"])[0])
    
    vis.scatter(mean, corr, labels, "mean", "R", "Correlation")
    plt.show()


        





    

    
