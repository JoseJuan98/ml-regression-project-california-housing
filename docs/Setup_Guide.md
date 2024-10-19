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