# Aim of this document

The aim is this document is to briefly present the code structure and how to set up and execute the examples.
It can serve as son kind of use guide.

# Project Structure

```bash
lab3
  ├── data/                                         # repository with the datasets in csv format
  │
  ├── plots/                                        # directory with the saved plots
  │     
  ├── environment.yaml                              # conda environment installation file
  │
  ├── main.py                                       # main script to execute all the examples
  ├── README.md                                     # this file, containing technical information about the project
  ├── requirements.txt                              # main dependencies in pip format 
  └── exper                                         # source code for the experiments library
      │
      ├──  
```

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




