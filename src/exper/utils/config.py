# -*- coding: utf-8 -*-
"""Config utils module."""

import tomllib
import pathlib


class Config:
    """Holds the configuration of the project.

    Desc:
        Gets the configuration from the `config.toml` file in the root project directory if not specified.
    """

    def __init__(self, cfg_file: str = None):
        """Load the config from the `config.toml` file.

        Args:
            cfg_file (optional, str): path to the `config.toml` file. Defaults to the `config.toml` root's directory.
        """
        if cfg_file is None:
            cfg_file = pathlib.Path(__file__).parent.parent.parent / "config.toml"

        with open(file=cfg_file, mode="rb") as f:
            parsed_cfg = tomllib.load(f)
            f.close()

        print(parsed_cfg)
