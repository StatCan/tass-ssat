from appium.webdriver.appium_service import AppiumService
from tass.core.log.logging import getLogger


class TASSAppiumService(AppiumService):

    logger = getLogger(__name__)

    def __init__(self, uuid, args):
        super().__init__()
        self._args = args
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @property
    def args(self):
        return self._args

    @classmethod
    def service(cls, driver, appium=None):
        DEFAULT = {
            "--log": "./logs/appium.log"
        }
        args = []
        if appium is not None:
            DEFAULT.update(appium)

        for k,v in DEFAULT.items():
            args.append(str(k))
            if not isinstance(v, bool):
                args.append(str(v))
        _uuid = driver.uuid + "-appium-service"
        service = cls(_uuid, args)
        return service

    @classmethod
    def start(cls, service):
        if service and service.is_running:
            cls.logger.debug("Appium Server is currently running: %s>%s", service.uuid, service)
            return None
        cls.logger.debug("Starting Appium Server %s: %s", service.uuid, service.args)
        _ = service.start(args=service.args)
        cls.logger.debug("Appium Server started: %s", _)
        return _

    @classmethod
    def stop(cls, service):
        if service and service.is_running:
            cls.logger.debug("Stopping Appium Server %s: %s", service.uuid, service)
            return service.stop()
        else:
            cls.logger.debug("Appium Server is not running: %s>%s", service.uuid, service)
            return False
