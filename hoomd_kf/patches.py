"""
This file contains the Patches class that holds a list of Patch objects.
Has the ability to generate C++ code to be compiled by hoomd.hpmc.
See: https://hoomd-blue.readthedocs.io/en/latest/tutorial/07-Modelling-Patchy-Particles/02-Simulating-a-System-of-Patchy-Particles.html
"""
import numpy as np
from hoomd_kf.patch import Patch
from hoomd_kf.utils import check_adjacency


class Patches:
    """
    A Patches object contains a list of Patch objects.
    """

    def __init__(self, list_of_patches=None):
        """
        Initialize the Patches object.
        """
        self.list_of_patches = list_of_patches
        self.n_patch = None
        if self.list_of_patches:
            self.n_patch = len(self.list_of_patches)
            self.check_data()
            self.check_patch_indices()

    def check_data(self):
        """
        Checks that the list of patches consists of Patch objects.
        """
        for i, patch_i in enumerate(self.list_of_patches):
            if not isinstance(patch_i, Patch):
                print(f"WARNING: patch index {i} is not a Patch object.")

    def check_patch_indices(self):
        """
        Checks that each patch has a unique index.
        """
        indices = []
        for i, patch_i in enumerate(self.list_of_patches):
            if patch_i.patch_type is None:
                patch_i.patch_type = i
                continue
            if patch_i.patch_type not in indices:
                indices.append(patch_i.patch_type)
            else:
                print("WARNING: clashing patch indices.")
                return

    def set_adjacency(self, adjacency_matrix):
        """
        Function that sets what patch interacts with what other patch
        based on an adjacency matrix.
        """
        adjacency_matrix = np.array(adjacency_matrix)

        if not check_adjacency(adjacency_matrix):
            return

        # clean interaction lists
        for i in range(self.n_patch):
            self.list_of_patches[i].interacts_with = []

        # set interaction lists based on the adjacency matrix provided
        for i in range(self.n_patch):
            for j in range(i, self.n_patch):
                if adjacency_matrix[i, j] == 1:
                    if j not in self.list_of_patches[i].interacts_with:
                        self.list_of_patches[i].interacts_with.append(j)
                    if i not in self.list_of_patches[j].interacts_with:
                        self.list_of_patches[j].interacts_with.append(i)

    def make_all_patches_interact_with_each_other(self):
        """
        Function that sets patch adjacency such that they all interact
        with each other.
        """
        adjacency = np.ones((self.n_patch, self.n_patch))
        self.set_adjacency(adjacency)
