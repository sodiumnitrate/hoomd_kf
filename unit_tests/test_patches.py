import numpy as np
from hoomd_kf.patches import Patches
from hoomd_kf.patch import Patch
from hoomd_kf.utils import check_adjacency

class TestPatches:
    def test_getitem_1(self):
        patch_1 = Patch()
        patch_2 = Patch()
        patch_3 = Patch()
        patch_4 = Patch()

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        patch = patches_obj[3]
        assert isinstance(patch, Patch)

    def test_getitem_2(self):
        patch_1 = Patch()
        patch_2 = Patch()
        patch_3 = Patch()
        patch_4 = Patch()

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        patches = patches_obj[:3]
        assert isinstance(patches, Patches)
        assert len(patches) == 3

    def test_getitem_3(self):
        patch_1 = Patch()
        patch_2 = Patch()
        patch_3 = Patch()
        patch_4 = Patch()

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        patches = patches_obj[:3]
        assert isinstance(patches, Patches)
        assert len(patches) == 3

    def test_adjacency(self):
        patch_1 = Patch()
        patch_2 = Patch()
        patch_3 = Patch()
        patch_4 = Patch()

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        patches_obj.make_all_patches_interact_with_each_other()

        assert patches_obj.list_of_patches[0].interacts_with == [0,1,2,3]
        assert patches_obj.list_of_patches[1].interacts_with == [0,1,2,3]
        assert patches_obj.list_of_patches[2].interacts_with == [0,1,2,3]
        assert patches_obj.list_of_patches[3].interacts_with == [0,1,2,3]

    def test_adjacency_2(self):
        patch_1 = Patch()
        patch_2 = Patch()
        patch_3 = Patch()
        patch_4 = Patch()

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        adjacency = [[1,0,1,0], [0,0,1,1], [1,1,0,0], [0,1,0,1]]

        patches_obj.set_adjacency(adjacency)

    def test_generate_simple_tetrahedral(self):
        patches_obj = Patches()
        patches_obj.generate_simple_tetrahedral()
        assert len(patches_obj) == 4
        vec = [0,0,0]
        for i in range(4):
            for j in range(3):
                vec[j] += patches_obj.list_of_patches[i].vec[j]
        assert np.isclose(vec[0], 0)
        assert np.isclose(vec[1], 0)
        assert np.isclose(vec[2], 0)

    def test_generate_simple_trivalent(self):
        patches_obj = Patches()
        patches_obj.generate_simple_trivalent()
        assert len(patches_obj) == 3
        vec = [0,0,0]
        for i in range(3):
            for j in range(3):
                vec[j] += patches_obj.list_of_patches[i].vec[j]
        assert np.isclose(vec[0], 0)
        assert np.isclose(vec[1], 0)
        assert np.isclose(vec[2], 0)

    def test_generate_bivalent(self):
        theta = 2.099
        patches_obj = Patches()
        patches_obj.generate_bivalent(theta=theta)
        assert len(patches_obj) == 2

        v1 = np.array(patches_obj.list_of_patches[0].vec)
        v2 = np.array(patches_obj.list_of_patches[1].vec)

        assert np.isclose(v1.dot(v1), 1)
        assert np.isclose(v2.dot(v2), 1)
        assert np.isclose(v1.dot(v2), np.cos(theta))

    def test_get_adjacency_from_patch_info(self):
        patch_1 = Patch()
        patch_1.interacts_with = [0, 2]
        patch_2 = Patch()
        patch_2.interacts_with = [3]
        patch_3 = Patch()
        patch_3.interacts_with = [0, 2]
        patch_4 = Patch()
        patch_4.interacts_with = [1, 3]

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        adjacency = patches_obj.get_adjacency_from_patch_info()
        assert check_adjacency(adjacency)

        compare = np.array([[1, 0, 1, 0], 
                            [0, 0, 0, 1],
                            [1, 0, 1, 0],
                            [0, 1, 0, 1]])

        assert np.array_equal(adjacency, compare)