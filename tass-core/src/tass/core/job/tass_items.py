

class TassItem():

    def __init__(self, parent=None, uuid=None, build=None,
                 title=None, **kwargs):
        self._parent = parent
        self._title = title
        self._uuid = uuid
        self._build = build
        self._var = kwargs

    @property
    def title(self):
        return self._title

    @property
    def uuid(self):
        return self._uuid

    @property
    def parent(self):
        return self._parent

    @property
    def build(self):
        return self._build

    def var(self, name):
        return self._var[name]

    @classmethod
    def from_parent(cls, parent,
                    title, uuid,
                    build=None,
                    **kwargs):

        _build = 'dev' if build is None else parent.build

        return cls(parent=parent, title=title,
                   uuid=uuid, build=_build,
                   **kwargs)

    @classmethod
    def create(cls, title, uuid,
               build='dev',
               **kwargs):

        return cls(parent=DefaultTassItem(), title=title,
                   uuid=uuid, build=build, **kwargs)


class DefaultTassItem(TassItem):

    def __init__(self):
        super().__init__(parent=None,
                         title='Default Tass Item',
                         uuid="!0001",
                         build="dev"
                         )


class TassFile(TassItem):

    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path
