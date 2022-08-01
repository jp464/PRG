# Installation and Usage

### Installation for Windows

First, install [Anaconda](https://www.anaconda.com/products/distribution) to set up the phd-report environment. 

Then, install [MiKTeX](https://miktex.org/howto/install-miktex) to set up the latex compiler. When using the installer, under settings, select "Yes" for "Install missing pacakages on-the-fly". After installation, please check for [updates](https://miktex.org/howto/update-miktex).

Now, open the command prompt. 

To use the phd-report-generator, download it:
```
(base) C:/Users/username> cd Desktop
(base) C:/Users/username/Desktop> git clone https://github.com/jp464/PRG.git
```

If you are unable to use git, download it from [here](https://github.com/jp464/PRG.git):
+ Click on the green box that reads "Code" and click "Download Zip"
+ Open the zip file and place inside your desktop

Create an environment:
```
(base) C:/Users/username> cd Desktop
(base) C:/Users/username/Desktop> cd PRG
(base) C:/Users/username/Desktop/PRG> cd report-generator
(base) c:/Users/username/PRG/report-generator> conda env create -f requirements.yml

```

Activate the environment:
```
(base) c:/Users/username/PRG/report-generator> activate PRG
```

### Usage
Run the flask application:
```
(base) c:/Users/username/PRG/report-generator> flask run
```

All the generated reports will be under:
```
C:/Users/username/Desktop/PRG/reports
```

*Note that the "School" and "Academic Divisions" filters are still in development. Please just use the "Individual Programs" filter for the time being.*
