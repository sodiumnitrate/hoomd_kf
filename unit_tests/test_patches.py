from unittest.mock import patch
from hoomd_kf.patches import Patches
from hoomd_kf.patch import Patch

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
        assert patches.n_patch == 3

    def test_getitem_3(self):
        patch_1 = Patch()
        patch_2 = Patch()
        patch_3 = Patch()
        patch_4 = Patch()

        patches_obj = Patches(list_of_patches=[patch_1, patch_2, patch_3, patch_4])

        patches = patches_obj[:3]
        assert isinstance(patches, Patches)
        assert patches.n_patch == 3

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