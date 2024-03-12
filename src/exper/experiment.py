# -*- coding: utf-8 -*-
"""Experiment definition class."""


class Experiment:
    """Experiment"""

    def __init__(self, experiment_name: str, experiment_description: str, steps: list) -> None:
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.steps = steps
