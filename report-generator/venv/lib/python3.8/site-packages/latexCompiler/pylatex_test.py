
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape 
import os 

PATH = os.path.dirname(os.path.abspath(__file__))
FILE_template = os.path.join(PATH, "title.tex")
FILE_style = os.path.join(PATH, "CSSullivanBusinessReport.cls")

Background = "The data that follows was collected via the Exit Survey for Ph.D. Completers. This survey was administered by The Graduate School to DEPARTMENT doctoral students graduating between 2017 and 2021.  Graduating doctoral students were invited to complete the survey in their final semester in the DEPARTMENT program.  Nineteen of the twenty DEPARTMENT program graduates (95 %) completed the Exit Survey for Ph.D. Completers."

# create document
doc = Document('basic')

# formatting
with open(FILE_style) as f:
       preamb = ''.join(f.readlines())
       doc.preamble.append(NoEscape(preamb))

# title
with open(FILE_template) as f:
    intro = ''.join(f.readlines())
    doc.append(NoEscape(intro))

# background
doc.append(NoEscape(r'\begin{fullwidth}'))
with doc.create(Section("Background")):
    doc.append(Background)
doc.append(NoEscape(r'\end{fullwidth}'))

doc.generate_pdf(filepath = "final-report", clean_tex = False)
