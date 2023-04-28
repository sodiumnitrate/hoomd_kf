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
                 interacts_with=None,
                 type=None):
        """
        Initialize patch object.
        """
        self.kf_lambda = kf_lambda
        self.cos_delta = cos_delta
        self.delta = delta
        self.interacts_with = interacts_with
        self.type = type
