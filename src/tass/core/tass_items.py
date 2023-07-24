import tass.config.browserconfig as browserconfig


class TassItem():


    def __init__(self, parent=None, name=None, uuid=None, build=None,
                 config=None):
        self._parent = parent
        self._name = name
        self._uuid = uuid
        self._build = build
        self._config = config

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

    @property
    def config(self):
        return self._config

    @classmethod
    def from_parent(cls, parent,
               name, uuid,
               build=None, config=None,
               **kwargs):
        if (config is None) and \
           (parent is not None) and \
           (parent.config is not None):
            _config = parent.config
        else:
            _config = browserconfig.load(config)

        _build = 'dev' if build is not None else parent.build


        return cls(parent=parent, name=name,
                   uuid=uuid, build=_build,
                   config=_config, **kwargs)

    @classmethod
    def create(cls, name, uuid,
               build='dev', config=None,
               **kwargs):
        _config = browserconfig.load(config)

        return cls(parent=DefaultTassItem(), name=name,
                   uuid=uuid, build=build,
                   config=_config, **kwargs)


class DefaultTassItem(TassItem):


    def __init__(self):
        super().__init__(parent=None,
                        name='Default Tass Item',
                        uuid="!0001",
                        build="dev",
                        config=browserconfig.load(None)
                        )


class TassFile(TassItem):

    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path
