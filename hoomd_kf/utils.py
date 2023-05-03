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