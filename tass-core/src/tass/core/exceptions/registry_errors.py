class TASSRegistryLookupError(LookupError):
    def __init__(self, *args):
        super().__init__(*args)

    
class TASSCommandNotFoundError(TASSRegistryLookupError):
    def __init__(self, *args):
        super().__init__(*args)


class NoSuchTASSRegistryError(TASSRegistryLookupError):
    def __init__(self, *args):
        super().__init__(*args)

