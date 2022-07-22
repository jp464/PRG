from asyncio.windows_events import NULL
from gettext import NullTranslations
import pandas as pd

class Input: 
    def __init__(self):
        self.df = NULL
        self.program = NULL
        self.years = NULL

    def __init__(self, df, program, years):
        self.df = df
        self.program = program
        self.years = years 

    def get_df(self, df):
        self.df = df

    def get_program(self, program):
        self.program = program

    def get_years(self, years):
        self.years = years

        
if __name__ == "__main__":
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)

    input = Input(df, "Biology", 2019)
    print(input.df, input.program, input.years)
