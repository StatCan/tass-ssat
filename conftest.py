from tass.core.tass_file import TassRun as Run


def pytest_collect_file(parent, file_path):
    if file_path.name.startswith('tass'):
        file = Run.from_parent(parent=parent, path=file_path)
        print(file)
        return file
