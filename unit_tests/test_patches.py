import copy
import numpy as np
from hoomd_kf.patches import Patches
from hoomd_kf.patch import Patch
from hoomd_kf.utils import check_adjacency

import pdb

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

    def test_update_interaction_indices(self):
        patches_obj = Patches()
        patches_obj.generate_simple_tetrahedral()

        indices = (0,2)
        new_patches = Patches()
        patch_0 = copy.copy(patches_obj.list_of_patches[0])
        patch_2 = copy.copy(patches_obj.list_of_patches[2])
        new_patches.list_of_patches = [patch_0, patch_2]
        new_patches.update_interaction_indices(indices)

        list_0 = new_patches.list_of_patches[0].interacts_with
        assert list_0[0] == 0
        assert list_0[1] == 1

        list_1 = new_patches.list_of_patches[1].interacts_with
        assert list_0[0] == 0
        assert list_0[1] == 1

        list_0_old = patches_obj.list_of_patches[0].interacts_with
        assert len(list_0_old) == 4

    def test_getitem_slice(self):
        patches_obj = Patches()
        patches_obj.generate_simple_tetrahedral()

        new_patches = patches_obj[:2]
        assert len(new_patches) == 2
        assert len(patches_obj) == 4

        new_patches = patches_obj[1:3]
        assert len(new_patches) == 2
        assert len(patches_obj) == 4

        new_patches = patches_obj[1:]
        assert len(new_patches) == 3
        assert len(patches_obj) == 4

    def test_getitem_int(self):
        patches_obj = Patches()
        patches_obj.generate_simple_tetrahedral()

        patch = patches_obj[0]
        assert isinstance(patch, Patch)
        assert len(patch.interacts_with) == 4

    def test_getitem_tuple(self):
        patches_obj = Patches()
        patches_obj.generate_simple_tetrahedral()

        new_patches = patches_obj[0,2,3]
        assert len(new_patches) == 3

        assert len(new_patches[0].interacts_with) == 3

    def test_getitem_2(self):
        patches_obj = Patches()
        patches_obj.generate_simple_tetrahedral()

        adjacency = np.array([[1, 0, 1, 0], 
                              [0, 0, 0, 1],
                              [1, 0, 1, 0],
                              [0, 1, 0, 1]])

        patches_obj.set_adjacency(adjacency)

        new_patches = patches_obj[:2]

        list_0 = new_patches[0].interacts_with
        assert len(list_0) == 1
        assert list_0[0] == 0
        list_1 = new_patches[1].interacts_with
        assert len(list_1) == 0

    def test_add(self):
        patches_1 = Patches()
        patches_1.generate_simple_tetrahedral()

        patches_2 = Patches()
        patches_2.generate_bivalent()

        total = patches_1 + patches_2

        assert len(total) == 6
        assert len(patches_1) == 4
        assert len(patches_2) == 2

    def test_add_2(self):
        patches_1 = Patches()
        patches_1.generate_bivalent()

        patches_2 = Patches()
        patches_2.generate_bivalent()

        total = patches_1 + patches_2

        list_0 = total[0].interacts_with
        list_3 = total[3].interacts_with

        assert len(list_0) == 2
        assert len(list_3) == 2

        assert list_3[0] == 2
        assert list_3[1] == 3