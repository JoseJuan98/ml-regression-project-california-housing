<h1 align="center">California Housing Census Project</h1>

<p align="center">Author: Jose Pena</p>
<p align="center">Github: <a href="https://github.com/JoseJuan98">JoseJuan98</a></p>
<br>

---

## Aim

The aim of this project is to showcase my analytical, technical, and communicative skills as a Machine Learning Engineer. I aim to demonstrate my ability to produce a successful and resilient Machine Learning system, from the exploratory and modeling phase focused on the exploration, statistical analysis, and good practices of Machine Learning, to the engineering phase to containerize all dependencies of the system and serve it in a production environment while giving concise and informative insights in a business-manner for non-technical stakeholders.

To differentiate between phases and follow good practices, I am following the Gitflow methodology. I develop new changes in feature branches and create pull requests to the branches develop and master to test the changes in a CI/CD pipeline and simulate the approval of the code/product owner (the CI/CD flow is not ready yet).

## Dataset

This California Housing dataset is available from [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) (University of Porto).

This dataset appeared in a 1997 paper titled "Sparse Spatial Autoregressions" by Pace, R. Kelley and Ronald Barry, published in the Statistics and Probability Letters journal. They built it using the 1990 California census data. It contains one row per census block group. A block group is the smallest geographical unit for which the U.S. Census Bureau publishes sample data (a block group typically has a population of 600 to 3,000 people).

The target variable or dependent variable for this analysis will be the `median_house_value`, which describes the median price of the houses per block group.

## File Structure

```shell
.
├── bin                 # Contains artifacts or produced metadata not relevant
│   
├── data                # Stores data used for cases (not necessary to store in repository, as the data is available by web)
│     
├── notebooks           # Notebooks used for exploration, experimentation, analysis, to finally produce the final model and put it into a production environment
│     │     
│     ├── ExploratoryDataAnalysis.ipynb     # Exploratory data analysis to discover insights and features about the variables used
│     │     
│     ├── RegressionAnalysis.ipynb         # Modeling experimentation to discover the most suitable models and fine-tune hyperparameters
│     │     
│     ├── Explainability.ipynb             # Explanation or brief understanding of the final model, parameters (variables), and hyperparameters 
│     │     
│     └── Old.ipynb                        # Previous work done (first ML case in 2019), kept to show myself how much I improved in the last years
│     
├── reports             # Contains generated reports
│     │
│     └── ExploratoryDataAnalysis.pdf
│     
├── src                 # Source code
│     ├── build_model.py
│     ├── preprocess.py
│     ├── feature_engineering.py
│     ├── evaluate.py
│     ├── __init__.py
│     ├── template.py
│     └── train.py
│     
├── test                # Test code
│     └── testTemplate.py
│     
├── utils               # Utility code
│     └── data_gathering.py
│     
└── README.md           # Project documentation
```

## Usage

The project can be used in two ways:

### 1. Jupyter Notebooks

To run the Jupyter notebooks, create a virtual environment and install the required packages as shown below:

```shell
# Install a python virtual environment manager
pip install virtualenv 
python -m virtualenv venv  

# Activate the virtual environment
source ./venv/bin/activate # Linux 
./bin/Scripts/activate     # Windows   

# Install the dependencies
python -m pip install -U pip pip install --no-cache-dir -r requirements/analysis.txt
```

Then navigate to the notebooks folder and launch Jupyter:

```shell
cd notebooks 
jupyterlab <notebook>
```


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Check list

This check-list shows the phases of the project that have been completed and the next steps:

- [X] Exploratory Data Analysis
- [ ] Machine Learning Modelling (Regression Analysis) -> In progress
- [ ] API development to expose the final model
- [ ] Containerization of the API to enable deployment it in any environment
- [ ] MLOps - CI/CD pipeline for ML operations

Other ideas to try in the project:

-   Use distributed ML tools like PySpark/Dask with Scalene Profiler to see if it improves training times and results
-   Develop 2 microservices that depend on each other to expose the model (one in Scala, another in Python for interoperability) and use ONNX for cross-platform models
-   Consider using GPU computing frameworks with native serving libraries to improve inferences using Scalene Profiler, even if it's overkill
-   Create a simple website to test different models with several microservices

[comment]: <> (For the MLOps phase check: https://github.com/outerbounds/full-stack-ML-metaflow-tutorial)


[comment]: <> (
    Description of the dataset: Add a brief overview of the dataset used for this project, including information on the source, size, and format of the data.
    Explanation of the evaluation metric: If you are using a specific evaluation metric to measure the performance of your model, it might be helpful to provide an explanation of how it works and why you chose it.
    Results: Include a summary of the results you obtained during the experimentation phase. You could add tables or visualizations to make it easier to interpret and understand the results.
    Model interpretation: If you have used any techniques to interpret your model, such as feature importance or SHAP values, consider adding a section to your README that explains what you did and why it is important.
    Deployment instructions: When you are ready to deploy your model, include instructions on how to set up the API and containerize the application. This can be helpful for anyone who wants to reproduce your work or use your model in their own applications.
    Future work: Finally, it can be useful to include a section that outlines potential future work that could be done to improve the model or extend the project. This can give readers an idea of where the project could go next and inspire them to contribute their own ideas.
)