import unittest
import importlib


appium_inst = importlib.util.find_spec("appium")

config = [
    # TODO: generic Android config
    # TODO: generic Apple config
]

pages = {
    # TODO: Find and define test pages
        # the-internet-herokuapp
        # UI Test Automation Playground
        # QA Practice
}

@unittest.skipUnless(appium_inst, "Appium is not installed.")
class TestAppium(unittest.TestCase):
    # TODO: setup & start/close appium
    pass


class TestAppiumStartupActions(TestAppium):
    def test_AppiumNewDriver(self):
        pass

    def test_AppiumLoadURL(self):
        pass


class TestAppiumBasicActions(TestAppium):
    def test_AppiumClose(self):
        pass

    def test_AppiumQuit(self):
        pass

    def test_AppiumClick(self):
        pass

    def test_AppiumWrite(self):
        pass

    def test_AppiumClear(self):
        pass


class TestAppiumReadOnlyActions(TestAppium):

    def test_AppiumReadAttribute(self):
        pass

    def test_AppiumReadCSS(self):
        pass


class TestAppiumWindowControlActions(TestAppium):

    def test_AppiumSwitchToFrameId(self):
        pass

    def test_AppiumSwitchToFrameElement(self):
        pass

    def test_AppiumSwitchWindowNoTitle(self):
        pass

    def test_AppiumSwitchWindowClosed(self):
        pass

    def test_AppiumSwitchWindowByTitle(self):
        pass

    def test_AppiumSwitchWindowByPageTitle(self):
        pass


class TestAppiumDropdownActions(TestAppium):

    def test_AppiumSelectDropdownByText(self):
        pass

    def test_AppiumSelectDropdownByValue(self):
        pass

    def test_AppiumSelectDropdownByIndex(self):
        pass


class TestAppiumAssertActions(TestAppium):

    def test_AppiumAssertTextDisplayedSuccess(self):
        pass

    def test_AppiumAssertPartialTextDisplayedSuccess(self):
        pass

    def test_AppiumAssertTextDisplayedSoftFailure(self):
        pass

    def test_AppiumAssertTextDisplayedFailure(self):
        pass

    def test_AppiumAssertExactTextDisplayedSuccess(self):
        pass

    def test_AppiumAssertExactTextDisplayedSoftFailure(self):
        pass

    def test_AppiumAssertExactTextDisplayedFailure(self):
        pass

    def test_AppiumAssertDisplayedSuccess(self):
        pass
    def test_AppiumAssertDisplayedFailed(self):
        pass

    def test_AppiumAssertDisplayedSoftSuccess(self):
        pass

    def test_AppiumAssertDisplayedSoftFailed(self):
        pass

    def test_AppiumAssertNotDisplayedSuccess(self):
        pass

    def test_AppiumAssertNotDisplayedFailed(self):
        pass

    def test_AppiumAssertNotDisplayedSoftSuccess(self):
        pass

    def test_AppiumAssertNotDisplayedSoftFailed(self):
        pass

    def test_AppiumAssertPageIsOpenByTitleSoftFailure(self):
        pass

    def test_AppiumAssertPageIsOpenByURLSoftFailure(self):
        pass

    def test_AppiumAssertPageIsOpenByElementSoftFailure(self):
        pass

    def test_AppiumAssertPageIsOpenByTitleSoftSuccess(self):
        pass

    def test_AppiumAssertPageIsOpenByURLSoftSuccess(self):
        pass

    def test_AppiumAssertPageIsOpenByElementSoftSuccess(self):
        pass

    def test_AppiumAssertPageIsOpenByTitleFailure(self):
        pass

    def test_AppiumAssertPageIsOpenByURLFailure(self):
        pass

    def test_AppiumAssertPageIsOpenByElementFailure(self):
        pass

    def test_AppiumAssertPageIsOpenByTitleSuccess(self):
        pass

    def test_AppiumAssertPageIsOpenByURLSuccess(self):
        pass

    def test_AppiumAssertPageIsOpenByElementSuccess(self):
        pass

    def test_AppiumAssertAttributeDisplayedSuccess(self):
        pass

    def test_AppiumAssertPartialAttributeDisplayedSuccess(self):
        pass

    def test_AppiumAssertAttributeDisplayedSoftFailure(self):
        pass

    def test_AppiumAssertAttributeDisplayedFailure(self):
        pass

    def test_AppiumAssertExactAttributeDisplayedSuccess(self):
        pass

    def test_AppiumAssertExactAttributeDisplayedSoftFailure(self):
        pass

    def test_AppiumAssertExactAttributeDisplayedFailure(self):
        pass


class AppiumScreenshotActions(TestAppium):

    def test_AppiumScreenshotPage(self):
        pass

    def test_AppiumScreenshotElement(self):
        pass


class TestAppiumAlertActions(TestAppium):

    def test_AppiumHandleAlertAccept(self):
        pass

    def test_AppiumHandleAlertAccept1(self):
        pass

    def test_AppiumHandleAlertAcceptStr(self):
        pass

    def test_AppiumHandleAlertDismiss(self):
        pass

    def test_AppiumHandleAlertDismiss0(self):
        pass

    def test_AppiumHandleAlertDismissStr(self):
        pass

    def test_AppiumHandleConfirmationAlertAccept(self):
        pass

    def test_AppiumHandleConfirmationAlertDismiss(self):
        pass

    def test_AppiumHandlePromptAlertAccept(self):
        pass

    def test_AppiumHandlePromptAlertDismiss(self):
        pass

    def test_AppiumAssertAlertDisplayedSoftFailure(self):
        pass

    def test_AppiumAssertAlertDisplayedHardFailure(self):
        pass

    def test_AppiumAssertAlertTextDisplayedSuccess(self):
        pass

    def test_AppiumAssertAlertPartialTextDisplayedSuccess(self):
        pass

    def test_AppiumAssertAlertTextDisplayedFailureSoft(self):
        pass

    def test_AppiumAssertAlertTextDisplayedFailure(self):
        pass