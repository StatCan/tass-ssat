from ..config import browserconfig as bc


class TassItem():

    def __init__(self, parent=None, uuid=None, build=None,
                 title=None, config=None):
        self._parent = parent
        self._title = title
        self._uuid = uuid
        self._build = build
        self._config = config

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

    @property
    def config(self):
        return self._config

    @classmethod
    def from_parent(cls, parent,
                    title, uuid,
                    build=None, config=None,
                    **kwargs):
        if (config is None) and \
           (parent is not None) and \
           (parent.config is not None):
            _config = parent.config
        else:
            _config = bc.load(config)

        _build = 'dev' if build is None else parent.build

        return cls(parent=parent, title=title,
                   uuid=uuid, build=_build,
                   config=_config, **kwargs)

    @classmethod
    def create(cls, title, uuid,
               build='dev', config=None,
               **kwargs):
        _config = bc.load(config)

        return cls(parent=DefaultTassItem(), title=title,
                   uuid=uuid, build=build,
                   config=_config, **kwargs)


class DefaultTassItem(TassItem):

    def __init__(self):
        super().__init__(parent=None,
                         title='Default Tass Item',
                         uuid="!0001",
                         build="dev",
                         config=bc.load(None)
                         )


class TassFile(TassItem):

    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path
