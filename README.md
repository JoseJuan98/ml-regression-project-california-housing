<h1 style="text-align:center">California Housing Census Project</h1>

<p style="text-align:center">Author: Jose Pena</p>
<p style="text-align:center">Github: <a href="https://github.com/JoseJuan98">JoseJuan98</a></p>
<br>

------------------------------------------------------------------------------------------------


## Aim

The aim of this project to showcase a high quality work ready to highlight my analytical, technical and communicative skills needed for producing a successful and resilient Machine Learning system, from the exploratory and
modelling phase focus in the exploration, statistical analysis and good practices of Machine Learning, to the engineering phase to containerize all dependencies of the system and put it into production exposing this work in
a resilient manner, meanwhile giving concise and informative insights in a business-manner for no technical stakeholders.

To differentiate between phases and follow good practices I am following the gitflow methodology, developing new changes in *feature branches*, and creating Pull Requests to the branch *develop* and *master* to test the changes 
in a CI/CD pipeline and simulating the approval of the code/product owner (the CI/CD flow is not.

## Dataset

This California Housing dataset is available from [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) (University of Porto).

This dataset appeared in a 1997 paper titled Sparse Spatial Autoregressions by Pace, R. Kelley and Ronald Barry, published in the Statistics and Probability Letters journal. They built it using the 1990 
California census data. It contains one row per census block group. A block group is the smallest geographical unit for which the U.S. Census Bureau publishes sample data (a block group typically has a 
population of 600 to 3,000 people).

The target variable or dependent variable for this analysis will be the `median_house_value`, which describes median price of the houses per block group.

## File Structure




## Check list

This check-list shows the phases of the project has been already done and the next steps:

- [X] Exploratory Data Analysis
- [ ] Machine Learning Modelling Experimentation -> Working on it
- [ ] API development to expose the final model
- [ ] Containerization of the API to be able to deploy it in any environment
- [ ] MLOps - CI/CD pipeline for ML operations

Other ideas to try in the project:

- Use distributed ML like PySpark/Dask with Scalene Profiler to check if it improves training times and the results
- Use a microservices architecture to develop 2 micro-services that depends on each other to expose the model (one in Scala, another in Python for interoperability)
  - Use ONNX for cross-platform models
- Even if it's overkill use a GPU computing framework to use their native serving libraries to check how it can improve inferences using Scalene profiler
- Create a simple website to try several micro-services with different models

[comment]: <> (For the MLOps phase check: https://github.com/outerbounds/full-stack-ML-metaflow-tutorial)

## File Structure

```shell
.
├── bin                                       -> contains artifacts or produced metadata not relevant
│   
├── data                                      -> stores data used for cases (not need to store in repository, the data is available by web)
│     
├── notebooks                                 -> notebooks used for exploration, experimentation, analysis, to finally produce the final model
│     │                                          and put it to a Production environment
│     │      
│     ├── ExploratoryDataAnalysis.ipynb          -> exploratory data analysis to discover insights and features about the variables used
│     │     
│     ├── RegressionAnalysis.ipynb         -> modelling experimentation to discover most suited models and fine-tune hyperparameters
│     │     
│     ├── Explainability.ipynb                   -> explanation or brief understanding of the final modell, parameters (variables) and hyperparameters 
│     │     
│     └── Old.ipynb                              -> previous work done (first ML case in 2019), kept to show myself how much I improved in the last years
│     
├── reports
│     │
│     └── ExploratoryDataAnalysis.pdf
│     
├── src
│     ├── build_model.py
│     ├── preprocess.py
│     ├── feature_engineering.py
│     ├── evaluate.py
│     ├── __init__.py
│     ├── template.py
│     └── train.py
│     
├── test
│     └── testTemplate.py
│     
├── utils
│     └── data_gathering.py
│     
└── README.md

```

## To develop analysis and find insights

Create a venv and install all the requirements needed for creating analysis and finding insights on jupyter notebooks:

```shell
pip install virtualenv
python -m virtualenv venv

source ./venv/bin.activate # Linux
./bin/Scripts/activate     # Windows
 
python -m pip install -U pip
pip install --no-cache-dir -r requirements/analysis.txt
```
