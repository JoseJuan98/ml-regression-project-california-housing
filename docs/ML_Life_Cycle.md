# ML Life Cycle

The Machine Learning Life Cycle is a series of steps that a Machine Learning Engineer follows to develop and deploy
machine learning models. The typical steps are:

1. **Data Collection**: Collect data from various sources and ensure it's in a usable format.
2. **Data Preparation**: Clean, preprocess, and transform the data for machine learning.
3. **Data Exploration**: Explore the data to gain insights and identify patterns.
4. **Model Development**: Train models on the prepared data using various machine learning algorithms.
5. **Model Evaluation**: Evaluate the performance of the trained model using various metrics.
6. **Model Deployment**: Deploy the trained model into a production environment and create an API that can be accessed
   by other applications.
7. **Model Monitoring and Maintenance**: Monitor the model's performance and retrain it with new data periodically to
   improve its performance.

These steps are iterative and require continuous improvement and refinement. As a Machine Learning Engineer, maybe it's
needed go back and forth between them until the desired results are achieved.

# Development methodology

To differentiate between phases and follow good practices, I am following the Gitflow methodology. I develop new changes
in feature branches and create pull requests to the branches develop and master to test the changes in a CI/CD pipeline
and simulate the approval of the code/product owner (the CI/CD flow is not ready yet).

