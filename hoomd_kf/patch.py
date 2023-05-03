"""
This file holds the Patch class and related methods.
"""
import numpy as np


class Patch:
    """
    Patch object contains parameters and interaction information
    for a patch of the Kern-Frenkel model.
    """

    def __init__(self,
                 kf_lambda=None,
                 cos_delta=None,
                 delta=None,
                 epsilon=None,
                 interacts_with=[],
                 patch_type=None,
                 vec=[1,0,0]):
        """
        Initialize the Patch object.
        """
        self.kf_lambda = kf_lambda
        self.cos_delta = cos_delta
        self.delta = delta
        self.interacts_with = interacts_with
        self.patch_type = patch_type
        self.epsilon = epsilon
        self.vec = vec

        self.check_angular_width()

    def check_angular_width(self):
        """
        Function to check the range of
        """
        if self.delta is None and self.cos_delta is None:
            print("WARNING: patch angular width not provided.")
            return

        if self.delta is None:
            self.delta = np.arccos(self.cos_delta)

        if self.cos_delta is None:
            self.cos_delta = np.cos(self.delta)

    def check_range(self):
        """
        Function to check the range of attractive interaction.
        """
        if self.kf_lambda is not None:
            if self.kf_lambda <= 1:
                print(f"WARNING: patch range = {self.kf_lambda} <= 1:")
