"""
This file contains the PatchySystem class that holds info
about the system to be simulated.
"""
import itertools
import random
import numpy as np
import gsd.hoomd
from hoomd_kf.patches import Patches

class PatchySystem:
    """
    A PatchySystem object contains system-related info.
    """

    def __init__(self,
                 num_particles=None,
                 density=None,
                 patches=None,
                 particle_types={'A':1.}):
        """
        Initialize the PatchySystem object.
        """
        self.num_particles = num_particles
        self.density = density
        self.patches = patches
        self.particle_types = particle_types

        self.snapshot = None
        
        self.check_particle_types()

    def check_particle_types(self):
        """
        Function to check that the particle types and their frequencies
        provided make sense.
        """
        if not isinstance(self.particle_types, dict):
            print("WARNING: particle_types should be a dict.")
            return
        tot_frac = 0
        for types in self.particle_types.keys():
            tot_frac += self.particle_types[types]

        if np.abs(tot_frac-1) > 1e-10:
            print(f"WARNING: sum of particle type fractions is {tot_frac}.")

    def generate_initial_configuration(self,
                                       file_name=None,
                                       mode='xb'):
        """
        Function to create a .gsd file with initial configurations
        """
        if file_name is None:
            file_name = "initial.gsd"

        m = (self.num_particles/2) ** (1./3)
        m = int(np.ceil(m))

        K = int(np.ceil(self.num_particles ** (1./3)))
        spacing = self.num_particles / (K * self.density)

        # to prevent overlaps
        assert spacing >= 1

        L = K * spacing
        x = np.linspace(-L/2, L/2, K, endpoint=False)

        position = list(itertools.product(x, repeat=3))
        position = position[0:self.num_particles]
        orientation = [(1,0,0,0)] * self.num_particles

        # gsd snapshot
        snapshot = gsd.hoomd.Frame()
        snapshot.particles.N = self.num_particles
        snapshot.particles.position = position
        snapshot.particles.orientation = orientation
        snapshot.configuration.box = [L, L, L, 0, 0, 0]

        # set types
        snapshot.particles.types = list(self.particle_types.keys())
        type_ids = []
        type_indices = {key:i for i, key in enumerate(self.particle_types.keys())}

        for particle_type, fraction in self.particle_types.items():
            N = int(np.round(fraction * self.num_particles))
            type_ids += [type_indices[particle_type]] * N

        random.shuffle(type_ids)

        snapshot.particles.typeid = type_ids

        with gsd.hoomd.open(name=file_name, mode=mode) as f:
            f.append(snapshot)

        self.snapshot = snapshot