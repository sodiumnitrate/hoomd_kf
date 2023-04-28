
class Patches:
    def __init__(self, list_of_patches=None):
        self.list_of_patches = None
        self.n_patch = None
        if self.list_of_patches:
            self.n_patch = len(self.list_of_patches)

