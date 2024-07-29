from . import reporter_factory


class ReporterRegistrar():

    def __init__(self):
        self._reporters = {}
    
    def register_reporter(self, uuid, 
                          type, package,
                          factory=reporter_factory,
                          *args, **kwargs):
        if uuid not in self._reporters:
            self._reporters[uuid] = factory.get_reporter(type=type,
                                                         package=package,
                                                         uuid=uuid,
                                                         *args, **kwargs)
            
    def get_reporter(self, uuid):
        return self._reporters.get(uuid, None)
        
    def iter_reporters(self):
        for reporter in self._reporters.values():
            yield reporter