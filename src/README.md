# Aim of this document

The aim is this document is to briefly present the code structure and how to set up and execute the examples.
It can serve as son kind of use guide.

# Project Structure

```bash
src
├── analysis                                     # directory with analysis done for the project (EDA, Feature Engineering)
│
├── artifacts
│  ├── data                                          # directory with the dataset in csv format
│  │
│  ├── plots                                         # directory with the saved plots
│       
├── environment.yaml                              # conda environment installation file
│
├── main.py                                       # main script to execute the analysis and experiments carried out for the project
│
├── README.md                                     # this file, containing technical information about the project
│
├── requirements                                  # folder with different dependencies in pip format
│ 
├── experiments                                   # folder with code for the experiment to compare a NN with a Linear Regression model.
│
└── exper                                         # source code for the experiments library

```

`exper` is a library created following Object-Oriented Programming (OOP) for making easier to experiment with different
models using the same data to be able to have consistent and reliable results.

# Setup

## Dependencies

There is a `requirements.txt` file with the main dependencies in case of managing dependencies with pip,
and a `environment.yaml` file with the conda format in case of conda is prefered.

For installing a virtual environment with conda:

```bash
conda env update --file environment.yaml
```

For another virtual environment manager like pyenv, venv or virtualenv, after creating and activating
the virtual environment, you can install the dependencies with pip by:

```bash
pip install -e .[cpu,dev,api,analysis]
```

## CUDA GPU support

After installing the environment in any way execute

```bash
-e .[gpu,dev,api,analysis]
```

This only affects the `tensorflow` library.

# Execution

The main program to run the examples is in the `main.py` script.




