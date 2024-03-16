
<h1 style="text-align: center" > D7054E Final Project Report </h1>  
<p style="text-align: center" > Jose Juan Pena Gomez (jospen-3)  </p>  
<h4 style="text-align: center" > Individual Project </h4>  
<h3 style="text-align: center" > March 17, 2024  </h3>
# Introduction



# Methodology


# California Census Housing Study



## Dataset

This California Housing dataset is available from [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) (University of Porto).  
  
This dataset appeared in a 1997 paper titled "Sparse Spatial Auto-regressions" by Pace, R. Kelley and Ronald Barry, published in the Statistics and Probability Letters journal. They built it using the 1990 California census data. It contains one row per census block group. A block group is the smallest geographical unit for which the U.S. Census Bureau publishes sample data (a block group typically has a population of 600 to 3,000 people).
  
The target variable or dependent variable for this analysis will be the `median_house_value`, which describes the median price of the houses per block group.  
  
The California Housing dataset is a collection of census data for the state of California, USA, from the 1990 census.   
It consists of one row per census block group, with each block group representing the smallest geographical unit for which sample data is published by the U.S. Census Bureau. The dataset was compiled by Pace and Barry and published in the Statistics and Probability Letters journal in 1997.   
  
The dataset contains several features, including the median income, median house age, and median number of rooms per house, among others.   
The target variable or dependent variable for this analysis is the `median_house_value` which represents the median price of the houses per block group.   
  
The dataset is available from the University of Porto by the [Luís Torgo's page](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) and is often used in regression analysis and machine learning tasks.

## Hypothesis

*Simple linear models, such as Linear Regression algorithms, performs better than complex non-linear models, such a neural networks*

## Implementation



## Results


### Analysis


### Models

In a regression analysis project, selecting appropriate evaluation metrics is crucial to determine the performance of the model. The evaluation metrics used for this project are:  
  
-   **Mean Squared Error (MSE)**: This metric calculates the average squared difference between the predicted and actual values. It penalizes larger errors more heavily than smaller ones.  
  
-   **Root Mean Squared Error (RMSE)**: This is the square root of the MSE, which gives us a measure of the average magnitude of the error in the same units as the target variable.  
     
-   **Mean Absolute Error (MAE)**: This metric calculates the absolute difference between the predicted and actual values, taking the average over all samples.  
     
-   **R-squared (R2)**: This metric measures the proportion of variance in the target variable that can be explained by the model. It ranges from 0 to 1, with higher values indicating better performance.  
  
When selecting an evaluation metric, it is important to consider the nature of the problem and the context of the application. For instance, if the cost of false negatives is much higher than false positives, it is preferable to optimize for reducing the MSE for values below a certain threshold. Similarly, if we are interested in identifying extreme values of the target variable, we may prefer to use the MAE instead of the MSE. It is also essential to consider the range and distribution of the target variable and any specific requirements or constraints of the project. The selection of the most appropriate evaluation metric can help to ensure that the model meets the desired level of performance for the given task.


### Hypothesis testing


# Discussion


# Conclusion

*Because of the limited scope of the project the hypothesis was limited to the performance of the models, but given more time it would have been interesting to see efficiency metrics like training time, memory usage, etc to a have a more detailed comparison.*


# References

