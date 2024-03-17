<h1 style="text-align: center">California Housing Census Project</h1>

<p style="text-align: center">Author: Jose Pena</p>
<p style="text-align: center">Github: <a href="https://github.com/JoseJuan98">JoseJuan98</a></p>

![](src/artifacts/plots/population_density_and_price.png)

---

## Aim

------------------------------

#TODO: **new aim** -> show that is possible to have a good quality analysis and solution while following good
engineering practices and that doesn't require much more extra time or effort and that long-term actually it will save
much more time when moving PoC to production.

> **I want to prove that you can have the best of the academic and engineering worlds without compromising any of them
** -> tired of being told the opposite (time how much time this project can take).

Applying good engineering practices while producing a good quality analysis takes practice and to be good at both, show
I want to demonstrate that I can do it.

Also, I want to prove that meanwhile Jupyter Notebooks are a great toold for exploratory analysis or other kind of
experimental tasks, are not totally necessary. And a good point to not using meanwhile any analysis is separating
the implementation and findings from the presentation. This allows a more flexible exploration while not considering
the presentation of this, excluding the visualization, allowing later to gather the findings and present them
in any format desirable with a cleaner presentation without code. This last, it can be something very valuable for
non-technical stakeholders.


----------------------------

The aim of this project is to showcase my analytical, technical, and communicative skills as a Machine Learning (ML)
Engineer.

There are several definitions of ML Engineer, in this case I refer to the conjuction of the fields
Computer Science, Data Science, Data Engineering and DevOps. Also, notice that particular skills related to some of
these fields conjuction like skills related ML, MLOps, Deep Learning, Cloud and some other skills shared like
Statistics, story telling, and more are also considered when refering to this role.

More specifically I aim to demonstrate my ability to produce a successful and resilient Machine Learning system, from
the exploratory and modeling phase focused on the exploration, statistical analysis, and good practices of
ML, to the engineering phase to containerize all dependencies of the system and serve it in a production environment
while giving concise and informative insights in a business-manner for non-technical stakeholders.

# Project Highlights

- For the presentation of the findings and results of the analysis carried out check `reports/`
- For technical documentation related with installation, microservice, ... check in `docs/`
- For the code related to any part check `src/`

## Interesting results

Using the California Housing dataset
from [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) (explained in more detailed
below), several model and techniques were compared and these are some of the highlights.

![](src/artifacts/plots/population_density_and_price.png)

#TODO ....

##     

## Dataset

This California Housing dataset is available
from [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) (University of Porto).

This dataset appeared in a 1997 paper titled "Sparse Spatial Autoregressions" by Pace, R. Kelley and Ronald Barry,
published in the Statistics and Probability Letters journal. They built it using the 1990 California census data. It
contains one row per census block group. A block group is the smallest geographical unit for which the U.S. Census
Bureau publishes sample data (a block group typically has a population of 600 to 3,000 people).

The target variable or dependent variable for this analysis will be the `median_house_value`, which describes the median
price of the houses per block group.

The California Housing dataset is a collection of census data for the state of California, USA, from the 1990 census.
It consists of one row per census block group, with each block group representing the smallest geographical unit for
which sample data is published by the U.S. Census Bureau. The dataset was compiled by Pace and Barry and published in
the Statistics and Probability Letters journal in 1997.

The dataset contains several features, including the median income, median house age, and median number of rooms per
house, among others.
The target variable or dependent variable for this analysis is the `median_house_value` which represents the median
price of the houses per block group.

The dataset is available from the University of Porto by
the [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) and is often used in regression
analysis and machine learning tasks.

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
├── exper                 # Source code
│     ├── build_model.py
│     ├── preprocess.py
│     ├── feature_engineering.py
│     ├── evaluate.py
│     ├── __init__.py
│     ├── template.py
│     └── train.py
│     
├── test                # Test code
│     └── test_template.py
│     
├── utils               # Utility code
│     └── data_gathering.py
│     
└── README.md           # Project documentation
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Check list

This check-list shows the phases of the project that have been completed and the next steps:

- [X] Exploratory Data Analysis
- [X] Regression Analysis/Machine Learning Modelling
- [ ] Apply best practices:
    - [ ] `TargetTransformer`
    - [ ] Use a python packaging and dependency manager like poetry
    - [ ] Make a decisions document explaining the importance of this decision
    - [ ] Subtituing notebooks for python scripts and Markdown files for report
    - [ ] Explain the reasons why this is better (better sharing, better documentation, better modularity since day
      0, ...)
- [ ] API and FrontEnd development to expose the final model -> In progress
- [ ] Containerization of the API to enable deployment it in any environment
- [ ] MLOps - Continuous Integration, Deployment and Training (CI CD CT) pipeline for ML operations

Other ideas to try in the project:

- Use [hiplot](https://github.com/facebookresearch/hiplot) for high-dimensional data visualization using parallel
  coordinates.
- Use [localstack](https://localstack.cloud/) for provisioning cloud services locally.
- Use distributed ML tools like PySpark/Dask with Scalene Profiler to see if it improves training times and results
- Develop 2 microservices that depend on each other to expose the model (one in Scala, another in Python for
  interoperability) and use ONNX for cross-platform models
- Consider using GPU computing frameworks with native serving libraries to improve inferences using Scalene Profiler,
  even if it's overkill. e.g. with skorch.
- Create a simple website to test different models with several microservices

## Evaluation Metrics

In a regression analysis project, selecting appropriate evaluation metrics is crucial to determine the performance of
the model. The evaluation metrics used for this project are:

- **Mean Squared Error (MSE)**: This metric calculates the average squared difference between the predicted and actual
  values. It penalizes larger errors more heavily than smaller ones.

- **Root Mean Squared Error (RMSE)**: This is the square root of the MSE, which gives us a measure of the average
  magnitude of the error in the same units as the target variable.

- **Mean Absolute Error (MAE)**: This metric calculates the absolute difference between the predicted and actual values,
  taking the average over all samples.

- **R-squared (R2)**: This metric measures the proportion of variance in the target variable that can be explained by
  the model. It ranges from 0 to 1, with higher values indicating better performance.

When selecting an evaluation metric, it is important to consider the nature of the problem and the context of the
application. For instance, if the cost of false negatives is much higher than false positives, it is preferable to
optimize for reducing the MSE for values below a certain threshold. Similarly, if we are interested in identifying
extreme values of the target variable, we may prefer to use the MAE instead of the MSE. It is also essential to consider
the range and distribution of the target variable and any specific requirements or constraints of the project. The
selection of the most appropriate evaluation metric can help to ensure that the model meets the desired level of
performance for the given task.

## Results

## Model Interpretation

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

### 2. Microservice with API

Check [Microservice documentation](docs/Microservice_Development_and_Deployment.md)

[comment]: <> (For the MLOps phase check: https://github.com/outerbounds/full-stack-ML-metaflow-tutorial)


[comment]: <> (
    Description of the dataset: Add a brief overview of the dataset used for this project, including information on the source, size, and format of the data.
    Explanation of the evaluation metric: If you are using a specific evaluation metric to measure the performance of your model, it might be helpful to provide an explanation of how it works and why you chose it.
    Results: Include a summary of the results you obtained during the experimentation phase. You could add tables or visualizations to make it easier to interpret and understand the results.
    Model interpretation: If you have used any techniques to interpret your model, such as feature importance or SHAP values, consider adding a section to your README that explains what you did and why it is important.
    Deployment instructions: When you are ready to deploy your model, include instructions on how to set up the API and containerize the application. This can be helpful for anyone who wants to reproduce your work or use your model in their own applications.
    Future work: Finally, it can be useful to include a section that outlines potential future work that could be done to improve the model or extend the project. This can give readers an idea of where the project could go next and inspire them to contribute their own ideas.
)

## Further work
