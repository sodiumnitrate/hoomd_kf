import os
from hoomd_kf.patchy_system import PatchySystem

class TestPatchySystem:
    def test_initial_configuration(self):
        test_system = PatchySystem(num_particles=100,
                                   density=0.1)

        test_system.generate_initial_configuration(file_name="aux_files/initial.gsd", mode='wb')

        # check that the file is created
        assert "initial.gsd" in os.listdir("aux_files")

        # check density
        rho = test_system.num_particles / test_system.snapshot.configuration.box[0]
        assert rho == test_system.density

        assert test_system.num_particles == len(test_system.snapshot.particles.position)

    def test_initial_configuration_2(self):
        test_system = PatchySystem(num_particles=100,
                                   density=0.1,
                                   particle_types={'A':0.5, 'B':0.5})

        test_system.generate_initial_configuration(file_name="aux_files/initial.gsd", mode='wb')
        type_ids = test_system.snapshot.particles.typeid

        assert list(type_ids).count(0) / test_system.num_particles == 0.5

    def test_initial_configuration_3(self):
        test_system = PatchySystem(num_particles=100,
                                   density=0.1,
                                   particle_types={'A':0.1, 'B':0.15, 'C':0.25, 'D':0.5})

        test_system.generate_initial_configuration(file_name="aux_files/initial.gsd", mode='wb')
        type_ids = test_system.snapshot.particles.typeid

        assert list(type_ids).count(0) / test_system.num_particles == 0.1
        assert list(type_ids).count(1) / test_system.num_particles == 0.15
        assert list(type_ids).count(2) / test_system.num_particles == 0.25
        assert list(type_ids).count(3) / test_system.num_particles == 0.5
        