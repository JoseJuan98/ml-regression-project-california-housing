# -*- coding: utf-8 -*-
"""Setup script."""
import pathlib
from typing import Union

import setuptools


# TODO: put the requirements here as it's cleaner or use poetry and manage them with a pyproject.toml
def get_req(file_path: Union[str, pathlib.Path]) -> list[str]:
    """Retrieve requirements from a pip-requirements file"""
    with open(file_path, "r") as file:
        reqs = [str(req) for req in file.readlines()]
    return reqs


project_path = pathlib.Path(__file__).parent

# read metadata from package
metadata = {}
with open(project_path / "exper" / "__version__.py") as file:
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
        license=metadata["__license__"],
        long_description=reamde,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(include=["exper"]),
        package_dir={"exper": "exper"},
        platforms=["unix", "linux", "cygwin", "win32"],
        python_requires=">=3.11",
        install_requires=get_req(file_path=project_path / "requirements" / "core.txt"),
        # additional requirements: to be isntall like '.[dev,analysis]'
        extras_require={
            # requirements for development (testing, CI, build, ...)
            "dev": get_req(file_path=project_path / "requirements" / "development.txt"),
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
