# -*- coding: utf-8 -*-
"""Config utils module."""

import tomllib
import pathlib

from dataclasses import dataclass


@dataclass
class DataConfig:
    """Data config class."""

    desc: str
    data_url: str
    target: str
    artifact_dir: str
    raw_data_file: str


@dataclass
class Config:
    """Holds the configuration of the project.

    Desc:
        Gets the configuration from the `config.toml` file in the root project directory if not specified.
    """

    data: DataConfig
    root_path: pathlib.Path

    def __init__(self, cfg_file: str = None):
        """Load the config from the `config.toml` file.

        Args:
            cfg_file (optional, str): path to the `config.toml` file. Defaults to the `config.toml` root's directory.
        """
        self.root_path = pathlib.Path(__file__).parents[2]
        if cfg_file is None:
            cfg_file = self.root_path / "config.toml"

        with open(file=cfg_file, mode="rb") as f:
            parsed_cfg = tomllib.load(f)
            f.close()

        # adding dir path to files
        parsed_cfg["data"]["artifact_dir"] = str(self.root_path / parsed_cfg["data"]["artifact_dir"])
        parsed_cfg["data"]["raw_data_file"] = str(
            self.root_path / parsed_cfg["data"]["artifact_dir"] / parsed_cfg["data"]["raw_data_file"]
        )

        self.data = DataConfig(*parsed_cfg["data"])
