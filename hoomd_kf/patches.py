"""
This file contains the Patches class that holds a list of Patch objects.
Has the ability to generate C++ code to be compiled by hoomd.hpmc.
See: https://hoomd-blue.readthedocs.io/en/latest/tutorial/07-Modelling-Patchy-Particles/02-Simulating-a-System-of-Patchy-Particles.html
"""
import numpy as np
from hoomd_kf.patch import Patch
from hoomd_kf.utils import check_adjacency, generate_patch_geometry, slice_to_indices


class Patches:
    """
    A Patches object contains a list of Patch objects.
    """

    def __init__(self, list_of_patches=None):
        """
        Initialize the Patches object.
        """
        self.list_of_patches = list_of_patches
        if self.list_of_patches:
            self.check_data()
            self.check_patch_indices()

    def __len__(self):
        """
        Function to return the number of patches.
        """
        return len(self.list_of_patches)

    def __getitem__(self, key):
        """
        Overload __getitem__ so that you can slice into Patches.
        """
        # TODO: update patch indices and list of interactions
        if isinstance(key, slice):
            indices = slice_to_indices(key, len(self.list_of_patches))
            new_list = [self.list_of_patches[ii] for ii in list(indices)]
            new_patches = Patches(list_of_patches=new_list)
            return new_patches
        elif isinstance(key, int):
            return self.list_of_patches[key]
        elif isinstance(key, tuple):
            new_list = [self.list_of_patches[ii] for ii in key]
            new_patches = Patches(list_of_patches=new_list)
            return new_patches
        else:
            raise TypeError

    def __add__(self, to_be_added):
        """
        Function that can be used to merge two Patches objects,
        or to add a new Patch to Patches.
        """
        if isinstance(to_be_added, Patches):
            # we have a Patches object
            n_to_add = len(to_be_added)
            for patch in to_be_added:
                for i in range(len(patch.interacts_with)):
                    patch.interacts_with[i] += n_to_add
            self.list_of_patches += to_be_added
        elif isinstance(to_be_added, Patch):
            # we have a Patch object
            self.list_of_patches.append(to_be_added)
        else:
            raise TypeError

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
        for i in range(len(self)):
            self.list_of_patches[i].interacts_with = []

        # set interaction lists based on the adjacency matrix provided
        for i in range(len(self)):
            for j in range(i, len(self)):
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
        adjacency = np.ones((len(self), len(self)))
        self.set_adjacency(adjacency)

    def generate_patches_from_geometry(self,
                                       n_patches,
                                       kf_lambda=1.1,
                                       epsilon=1,
                                       cos_delta=0.92,
                                       theta=None):
        """
        Function that uses utils.generate_patch_geometry() to 
        create a list of patches.
        """
        vecs = generate_patch_geometry(n_patches, theta=theta)
        patch_list = []
        for i in range(n_patches):
            vec = vecs[i]
            patch = Patch(kf_lambda=kf_lambda,
                          cos_delta=cos_delta,
                          epsilon=epsilon,
                          patch_type=i,
                          vec=vec)
            patch_list.append(patch)

        self.list_of_patches = patch_list
        self.make_all_patches_interact_with_each_other()

    def generate_simple_tetrahedral(self,
                                    kf_lambda=1.1,
                                    epsilon=1,
                                    cos_delta=0.92):
        """
        Function to populate Patches object with a set of tetrahedral
        patches that interact with each other.
        """
        self.generate_patches_from_geometry(4,
                                            kf_lambda=kf_lambda,
                                            epsilon=epsilon,
                                            cos_delta=cos_delta)

    def generate_simple_trivalent(self,
                                  kf_lambda=1.1,
                                  epsilon=1,
                                  cos_delta=0.92):
        """
        Function to populate Patches object with patches such that
        3 patches equally spaced around the equator is are created.
        """
        self.generate_patches_from_geometry(3,
                                            kf_lambda=kf_lambda,
                                            epsilon=epsilon,
                                            cos_delta=cos_delta)

    def generate_bivalent(self,
                          kf_lambda=1.1,
                          epsilon=1,
                          cos_delta=0.92,
                          theta=None):
        """
        Function to populate Patches object with two patches separated
        by theta. If theta is None, the patches are separated by pi.
        """
        self.generate_patches_from_geometry(2,
                                            kf_lambda=kf_lambda,
                                            epsilon=epsilon,
                                            cos_delta=cos_delta,
                                            theta=theta)


    def get_adjacency_from_patch_info(self):
        """
        Function that goes through the list of interactions for all
        patches and creates an adjacency matrix.
        """
        n_patch = len(self)
        adjacency = np.zeros((n_patch, n_patch))
        for i, patch in enumerate(self.list_of_patches):
            for j in patch.interacts_with:
                adjacency[i,j] = 1

        return adjacency