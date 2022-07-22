// ========================================================================
// CONST VARIABLES
// ========================================================================
const schools = ["Fuqua", "Medicine", "Nicholas", "Nursing", "Pratt", "Sanford", "Trinity"]
const academic_divisions = ["Humanities", "Biological and Biomedical Sciences", "Physical Sciences and Engineering", "Social Sciences"]
const individual_programs = {"Humanities": ["Art, Art History and Visual Studies", "German Studies", "Philosophy", "Romance Studies", "Classical Studies", "English", "Literature", "Music", "Religion"], 
"Biological and Biomedical Sciences": ["Biochemistry", "Biology", "Biostatistics","Cell Biology", "Computational Biology and Bioinformatics", "Ecology", "Evolutionary Anthropology", "Genetics and Genomics", "Immunology", "Medical Physics", "Molecular Cancer Biology", "Molecular Genetics and Microbiology", "Neurobiology", "Pathology", "Pharmacology", "Population Health Sciences"], 
"Physical Sciences and Engineering": ["Biomedical Engineering", "Chemistry", "Civil and Environmental Engineering", "Computer Science", "Earth and Climate Sciences", "Electrical and Computer Engineering", "Environment", "Marine Science and Conservation", "Mathematics", "Mechanical Engineering and Materials Science", "Physics", "Statistical Science"], 
"Social Sciences": ["Business Administration", "Cultural Anthropology", "Economics", "Environmental Policy", "History", "Nursing", "Political Science", "Psychology and Neuroscience", "Public Policy Studies", "Sociology"]}
// ========================================================================
// Helper Functions
// ========================================================================
function createForm(list, ind) {
    var div = document.getElementById("chosenProgram")
    var newSelect = document.createElement("select");
    newSelect.setAttribute("name", "filter1")
    newSelect.setAttribute("style", "height:300px")
    newSelect.setAttribute("multiple", "multiple");

    if (ind == 1) {
        for (var val in list) {
            var opt_group = document.createElement("optgroup");
            opt_group.label = val;
            newSelect.appendChild(opt_group);

            programs = list[val]
            for (var program of programs) {
                var newOption = document.createElement("option");
                newOption.text = program;
                opt_group.appendChild(newOption);
            }
            
        }
    }

    else {
        for (var val of list) {
            var newOption = document.createElement("option");
            newOption.text = val;
            newSelect.appendChild(newOption);
        }
    }
    
    div.appendChild(newSelect);
}

function chooseProgram() {
    div = document.getElementById("chosenProgram");
    while (div.hasChildNodes()) div.removeChild(div.firstChild);

    var elem = document.getElementById("program");
    selected = elem.value;

    if (selected == "School") {
        createForm(schools, 0);
    }

    if (selected == "Academic-division") {
        createForm(academic_divisions, 0);
    }

    if (selected == "Individual-programs") {
        createForm(individual_programs, 1);
    }
}




