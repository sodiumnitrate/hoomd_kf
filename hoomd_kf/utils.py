"""
Contains utility functions for the hoomd_kf module.
"""
import numpy as np
from scipy.linalg import issymmetric

def check_adjacency(adjacency):
    """
    Given a matrix, checks that it fulfills the criteria
    for being an adjacency matrix:
        0- 2-dimensional
        1- m by m
        2- contains 1s and 0s only
        3- symmetric
    """

    adjacency = np.array(adjacency)

    shape = adjacency.shape

    if len(shape) != 2:
        print("ERROR: adjacency matrix must be 2-dimensional.")
        return False

    if shape[0] != shape[1]:
        print("ERROR: adjacency matrix must be square.")
        return False

    if False in (adjacency == 1) | (adjacency == 0):
        print("ERROR: adjacency matrix should contain only 0s and 1s.")
        return False

    # TODO: may want to relax this condition in the future
    # if the adjacency matrices become gigantic and sparse, use other methods to check for this
    if not issymmetric(adjacency):
        print("ERROR: adjacency matrix must be symmetric.")
        return False

    return True

def slice_to_indices(key, n_el):
    """
    Function that converts a slice object to a list of
    indices.
    """
    assert isinstance(key, slice)

    if key.step is None:
        step = 1
    else:
        step = key.step

    if key.start is None:
        start = 0
    else:
        start = key.start

    if key.stop is None:
        stop = n_el
    else:
        stop = key.stop

    return list(range(start, stop, step))

def generate_patch_geometry(n_patches, theta=None):
    """
    Function to generate some basic patch geometries.
    Works until N=4:
    - N=1, single patch
    - N=2, two patches, can be separated by an angle theta, if provided.
    - N=3, 3 patches forming a triangle at the equator
    - N=4, tetrahedral arrangement
    """
    # TODO: implement N=5 and N=6 as well
    if n_patches > 4:
        print("ERROR: can't generate patch geometry beyond n_patch=6.")
        return None
    if n_patches > 2 and theta is not None:
        print("WARNING: I can only generate regular shapes beyond n_patch=2, ignoring theta.")
    if n_patches == 1:
        return [[1,0,0]]
    if n_patches == 2:
        if theta is None:
            vec1 = [1,0,0]
            vec2 = [-1,0,0]
            vectors = [vec1, vec2]
            return vectors
        else:
            vec1 = [1,0,0]
            vec2 = [np.cos(theta), np.sin(theta), 0]
            vectors = [vec1, vec2]
            return vectors
    elif n_patches == 3:
        theta = 2*np.pi/3
        vec1 = [1,0,0]
        vec2 = [np.cos(theta),0,np.sin(theta)]
        vec3 = [np.cos(theta),0,-np.sin(theta)]
        return [vec1, vec2, vec3]
    elif n_patches == 4:
        vec1 = [1,0,0]
        cos_theta = -1/3
        theta = np.arccos(cos_theta)
        vec2 = [np.cos(theta), 0, np.sin(theta)]
        v3z = (np.cos(theta)-np.cos(theta)**2)/np.sin(theta)
        v3y = np.sqrt(1-np.cos(theta)**2-v3z**2)
        vec3 = [np.cos(theta), v3y, v3z]
        vec4 = [np.cos(theta), -v3y, v3z]
        vectors = [vec1, vec2, vec3, vec4]
        return vectors