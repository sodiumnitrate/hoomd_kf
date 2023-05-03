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

        kf_lambda -> range of square well interaction in units of diameter. Always > 1.
        cos_delta -> cos of angular width of patch
        delta -> angular width of patch
        interacts_with -> list of patches (in terms of indices within a patches object) the patch interacts with
        epsilon -> depth of the square well attraction
        vec -> vector that positions the patch on the particle.
        """
        self.kf_lambda = kf_lambda
        self.cos_delta = cos_delta
        self.delta = delta
        self.interacts_with = interacts_with
        self.epsilon = epsilon
        self.patch_type = patch_type
        self.vec = vec

        self.check_angular_width()
        self.check_range()

    def __repr__(self):
        """
        __repr__ function for Patch object.
        """
        return f"<Patch object of type {self.patch_type} at {hex(id(self))}>"

    def __str__(self):
        """
        __str__ function for Patch object.
        """
        return f"Patch object of type {self.patch_type}."

    def print_info(self):
        """
        Function to print patch info.
        """
        print(f"lambda:\t{self.kf_lambda}")
        print(f"cos_delta:\t{self.cos_delta}")
        print(f"epsilon:\t{self.epsilon}")
        print(f"patch type:\t{self.patch_type}")
        print(f"vec:\t({self.vec[0]}, {self.vec[1]}, {self.vec[2]})")
        interacts_with_string = "interacts with:\t"
        for i in self.interacts_with:
            interacts_with_string += f"{i},"
        interacts_with_string = interacts_with_string.strip(',')
        print(interacts_with_string)

    def check_angular_width(self):
        """
        Function to check the provided angular width, if any.
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

    def single_bond_per_patch(self):
        """
        Function to check whether the given patch range and angular
        width allows for only one bond per patch.
        """
        if self.kf_lambda is None:
            print("ERROR: I need kf_lambda to check single-bond-per-patch.")
            return False
        
        if self.delta is None and self.cos_delta is None:
            print("ERROR: I need a patch angular width to check single-bond-per-patch.")
            return False

        if self.cos_delta is None:
            sin_delta = np.sin(self.delta)

        if self.delta is None:
            sin_delta = np.sin(np.acos(self.cos_delta))

        sin_delta = np.sin(self.delta)
        
        if sin_delta <= 1/(2*self.kf_lambda):
            return True
        else:
            return False