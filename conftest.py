import pytest
from tass.core.tass_file import TassRun as Run
from tass.drivers.browserdriver import newDriver


def pytest_collect_file(parent, file_path):
    if file_path.name.startswith('tass'):
        file = Run.from_parent(parent=parent, path=file_path)
        print(file)
        return file


@pytest.fixture(autouse=True)
def setup_teardown(request):
    print('* * * * * * * * * * * * * * * * * * * *')
    print('')
    print('Running Test:', request.node.name)
    print('')
    print('* * * * * * * * * * * * * * * * * * * *')
    request.node.driver = newDriver(**request.node.browser_config)
    yield
    print('* * * * * * * * * * * * * * * * * * * *')
    print('')
    print('Finished Test:', request.node.name)
    print('')
    print('* * * * * * * * * * * * * * * * * * * *')
    request.node.driver.quit()
