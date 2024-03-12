# -*- coding: utf-8 -*-
"""Setup script."""
import pathlib
import setuptools

from typing import Union


def get_req(file_path: Union[str, pathlib.Path]) -> list[str]:
    """Retrieve requirements from a pip-requirements file"""
    with open(file_path, "r") as file:
        reqs = [str(req) for req in file.readlines()]
    return reqs


project_path = pathlib.Path(__file__).parent

# read metadata from package
metadata = {}
with open(project_path / "src" / "exper" / "__version__.py") as file:
    exec(file.read(), metadata)

with open(project_path / "README.md") as file:
    reamde = file.read()

if __name__ == "__main__":
    setuptools.setup(
        name=metadata["__title__"],
        description=metadata["__description__"],
        version=metadata["__version__"],
        author=metadata["__author__"],
        author_email=metadata["__author_email__"],
        # url=metadata["__url__"],
        license=metadata["__license__"],
        long_description=reamde,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        platforms=["unix", "linux", "cygwin", "win32"],
        python_requires=">=3.11",
        install_requires=get_req(file_path=project_path / "requirements" / "core.txt"),
        # additional requirements: to be isntall like '.[dev,analysis]'
        extras_require={
            # requirements for development (testing, CI, build, ...)
            "dev": get_req(file_path=project_path / "requirements" / "development.txt"),
            # requirements for data analysis and exploration using jupyter notebooks
            "analysis": get_req(file_path=project_path / "requirements" / "analysis.txt"),
            # requirements for the Rest API in the microservice
            "api": get_req(file_path=project_path / "requirements" / "api.txt"),
            # requirements for working with Neural Networks with CPU
            "cpu": get_req(file_path=project_path / "requirements" / "cpu.txt"),
            # requirements for working with Neural Networks with CUDA enabled GPU
            "cuda": get_req(file_path=project_path / "requirements" / "cuda.txt"),
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Engineers",
            "Natural Language :: English",
            "License :: OSI Approved :: TBD",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ],
    )
