import numpy as np
from hoomd_kf.utils import check_adjacency

class TestUtils:
    def test_check_adjacency(self):
        adjacency = [1,2,3]
        assert not check_adjacency(adjacency)

        adjacency = [[1,2], [1,3]]
        assert not check_adjacency(adjacency)

        adjacency = [[0,0],[1,1]]
        assert not check_adjacency(adjacency)

        adjacency = [[1,0],[0,1]]
        assert check_adjacency(adjacency)