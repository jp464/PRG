class Input: 

    def __init__(self, df_n=None, df_t=None, program=None, years=None):
        self.df_n = df_n
        self.df_t = df_t
        self.program = program
        self.years = years 

    def get_df_t(self, df):
        self.df_t = df

    def get_df_n(self, df):
        self.df_n = df

    def get_program(self, program):
        self.program = program

    def get_years(self, years):
        self.years = years

        
