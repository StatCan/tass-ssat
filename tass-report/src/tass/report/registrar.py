class ReporterRegistrar():

    def __init__(self):
        self._reporters = {}
    
    def register_reporter(self, id, cls, *args, **kwargs):
        if id not in self._reporters:
            self._reporters[id] = cls(*args, **kwargs)
            
    def get_reporter(self, id):
        return self._reporters.get(id, None)
        
    def iter_reporters(self):
        for reporter in self._reporters:
            yield reporter