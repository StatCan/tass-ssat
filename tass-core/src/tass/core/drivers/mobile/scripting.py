import subprocess
from ...log.logging import getLogger
from ..scripting import DriverScriptExecutor

log = getLogger(__name__)

class MobileDriverScriptExecutor(DriverScriptExecutor):
    pass


class AndroidDriverScriptExecutor(MobileDriverScriptExecutor):
    """
    Functions for executing scripts in preparation for the driver launching or closing.
    Scripts are highly controlled at this time, to prevent malicious
    or accidental actions being executed.
    """

    @classmethod
    def reset_chrome(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.warning("No device ID found for driver wrapper %s. Cannot reset Chrome.", driver_wrapper.uuid)
            return "Failed"
        log.debug("Clearing Chrome data for device: %s", device_id)
        # TODO: Use adb to clear chrome data
        return subprocess.run(f"adb -s {device_id} shell pm clear com.android.chrome".split())

    @classmethod
    def debug_chrome(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.warning("No device ID found for driver wrapper %s. Cannot set Chrome as debug app.", driver_wrapper.uuid)
            return "Failed"
        log.debug("Setting Chrome as app under test for device: %s", device_id)
        # TODO: Use adb to set chrome as app to test
        return subprocess.run(f"adb -s {device_id} shell am set-debug-app --persistent com.android.chrome".split())


    @classmethod
    def allow_chrome_notifications(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.warning("No device ID found for driver wrapper %s. Cannot set Chrome notifications permission.", driver_wrapper.uuid)
            return "Failed"
        log.debug("Granting notifications permissions to Chrome for device: %s", device_id)
        # TODO: Use adb to set chrome notifications permission to allowed
        return subprocess.run(f"adb -s {device_id} shell pm grant com.android.chrome android.permission.POST_NOTIFICATIONS".split())

    @classmethod
    def disallow_chrome_notifications(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.warning("No device ID found for driver wrapper %s. Cannot revoke Chrome notifications permission.", driver_wrapper.uuid)
            return "Failed"
        log.debug("Revoking notifications permissions to Chrome for device: %s", device_id)
        # TODO: Use adb to set chrome notifications permission to revoked
        return subprocess.run(f"adb -s {device_id} shell pm revoke com.android.chrome android.permission.POST_NOTIFICATIONS".split())

class IOSDriverScriptExecutor(MobileDriverScriptExecutor):
    pass