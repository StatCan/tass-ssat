from tass.core.tass_items import TassItem
from tass.drivers.browserdriver import newDriver
from tass.actions.actions import action


class TassCase(TassItem):
    def execute_tass(self):
        # print(self.steps)
        for step in self._steps:
            print('')
            print('* * * * * * * * * *')
            print(step)
            print('* * * * * * * * * *')
            _execute_step(step, self.driver)

    def __init__(self, *, steps=[], browser_config={}, **kwargs):
        # TODO: Include Pages after confirming data structure
        super().__init__(**kwargs)
        self._browser_config = browser_config
        self._steps = steps
        self._driver = None

    @property
    def driver(self):
        if (self._driver is None):
            self._driver = newDriver(**self._browser_config)
        return self._driver


def _execute_step(step, driver):
    params = dict(zip(it := iter(step.get('parameters', None)), it))
    action(*step.get('action'))(driver=driver, **params)
