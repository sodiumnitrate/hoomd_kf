import numpy as np
from hoomd_kf.utils import check_adjacency
from hoomd_kf.utils import generate_patch_geometry

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

    def test_generate_patch_geometry_1(self):
        vecs = generate_patch_geometry(1)
        assert len(vecs) == 1
        assert vecs[0][0] == 1
        assert vecs[0][1] == 0
        assert vecs[0][2] == 0

    def test_generate_patch_geometry_2(self):
        vecs = generate_patch_geometry(2)
        assert len(vecs) == 2
        v1 = np.array(vecs[0])
        v2 = np.array(vecs[1])
        assert v1.dot(v2) == -1
        assert v1.dot(v1) == 1
        assert v2.dot(v2) == 1

    def test_generate_patch_geometry_3(self):
        theta = 2.099
        vecs = generate_patch_geometry(2,theta=theta)
        assert len(vecs) == 2
        v1 = np.array(vecs[0])
        v2 = np.array(vecs[1])
        assert v1.dot(v2) == np.cos(theta)
        assert v1.dot(v1) == 1
        assert v2.dot(v2) == 1

    def test_generate_patch_geometry_4(self):
        vecs = generate_patch_geometry(3)
        assert len(vecs) == 3
        v1 = np.array(vecs[0])
        v2 = np.array(vecs[1])
        v3 = np.array(vecs[2])
        assert v1.dot(v2) == np.cos(2*np.pi/3)
        assert v1.dot(v3) == np.cos(2*np.pi/3)
        assert v1.dot(v1) == 1
        assert v2.dot(v2) == 1
        assert v3.dot(v3) == 1

    def test_generate_patch_geometry_5(self):
        vecs = generate_patch_geometry(4)
        assert len(vecs) == 4
        v1 = np.array(vecs[0])
        v2 = np.array(vecs[1])
        v3 = np.array(vecs[2])
        v4 = np.array(vecs[3])

        assert np.isclose(v1.dot(v2),-1./3)
        assert np.isclose(v1.dot(v3),-1./3)
        assert np.isclose(v1.dot(v4),-1./3)
        assert v1.dot(v1) == 1
        assert v2.dot(v2) == 1
        assert v3.dot(v3) == 1
        assert v4.dot(v4) == 1