class TassItem():

    def __init__(self, parent=None, name=None, uuid=None, build=None):
        self._parent = parent
        self._name = name
        self._uuid = uuid
        self._build = build if build else parent.build

    @property
    def name(self):
        return self._name

    @property
    def uuid(self):
        return self._uuid

    @property
    def parent(self):
        return self._parent

    @property
    def build(self):
        return self._build


class TassFile(TassItem):

    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path
