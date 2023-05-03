from hoomd_kf.patch import Patch

class TestPatch:
    def test_patch_single_bond_per_patch(self):
        patch = Patch(kf_lambda=1.1,
                      cos_delta=0.92)

        assert patch.single_bond_per_patch()
