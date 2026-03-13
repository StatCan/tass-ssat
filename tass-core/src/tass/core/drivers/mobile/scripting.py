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
            log.debug("No device ID found for driver wrapper %s.", driver_wrapper.uuid)
            log.debug("Clearing Chrome data for default device.")
            script = "adb shell pm clear com.android.chrome"
        else:
            script = f"adb -s {device_id} shell pm clear com.android.chrome"
            log.debug("Clearing Chrome data for device: %s", device_id)
        return subprocess.run(script.split())

    @classmethod
    def debug_chrome(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.debug("No device ID found for driver wrapper %s.", driver_wrapper.uuid)
            log.debug("Setting Chrome as app under test for default device.")
            script = "adb shell am set-debug-app --persistent com.android.chrome"
        else:
            log.debug("Setting Chrome as app under test for device: %s", device_id)
            script = f"adb -s {device_id} shell am set-debug-app --persistent com.android.chrome"
        return subprocess.run(script.split())


    @classmethod
    def allow_chrome_notifications(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.debug("No device ID found for driver wrapper %s.", driver_wrapper.uuid)
            log.debug("Granting notifications permissions to Chrome for default device.")
            script = "adb shell pm grant com.android.chrome android.permission.POST_NOTIFICATIONS"
        else:
            log.debug("Granting notifications permissions to Chrome for device: %s", device_id)
            script = f"adb -s {device_id} shell pm grant com.android.chrome android.permission.POST_NOTIFICATIONS"
        # TODO: Use adb to set chrome notifications permission to allowed
        return subprocess.run(script.split())

    @classmethod
    def disallow_chrome_notifications(cls, driver_wrapper):
        device_id = driver_wrapper.device_id
        if not device_id:
            log.debug("No device ID found for driver wrapper %s.", driver_wrapper.uuid)
            log.debug("Revoking notifications permissions to Chrome for default device.")
            script = "adb shell pm revoke com.android.chrome android.permission.POST_NOTIFICATIONS"
        else:
            log.debug("Revoking notifications permissions to Chrome for device: %s", device_id)
            script = f"adb -s {device_id} shell pm revoke com.android.chrome android.permission.POST_NOTIFICATIONS"
        return subprocess.run(script.split())

class IOSDriverScriptExecutor(MobileDriverScriptExecutor):
    pass