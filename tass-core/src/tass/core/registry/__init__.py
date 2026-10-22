from .broker import BrokerRegistry
from .commands import CommandBroker, SeleniumCommandBroker, FinderBroker as FBroker
from .hooks import HookBroker


CommandRegistry = BrokerRegistry()
SeleniumFinders = FBroker("tass.core.actions.locate.selenium_locate")
AppiumFinders = FBroker("tass.core.actions.locate.appium_locate")

# Selenium modules
# Selenium should contain all commands
# Selwait and selchain commands can easily be accessed via selenium
SeleniumBroker = CommandRegistry.register("selenium", "core", "tass.core.actions.browser.selenium", broker=SeleniumCommandBroker, default_retries=1, finder=SeleniumFinders)
SeleniumWaitBroker = CommandRegistry.register("selwait", "selenium", "tass.core.actions.browser.selenium_wait", broker=SeleniumCommandBroker, finder=SeleniumFinders)
SeleniumChainBroker = CommandRegistry.register("selchain", "selenium", "tass.core.actions.browser.selenium_chain", broker=SeleniumCommandBroker, finder=SeleniumFinders)

# Appium modules
# appium should contain all commands
# appwait and appchain commands can easily be accessed via appium
# appium fallsback to default selenium commands
AppiumBroker = CommandRegistry.register("appium", "selenium", "tass.core.actions.mobile.appium", broker=SeleniumCommandBroker, default_retries=1, finder=AppiumFinders)
AppiumWaitBroker = CommandRegistry.register("appwait", "appium", "tass.core.actions.mobile.appium_wait", broker=SeleniumCommandBroker, finder=AppiumFinders)
AppiumChainBroker = CommandRegistry.register("appchain", "appium", "tass.core.actions.mobile.appium_chain", broker=SeleniumCommandBroker, finder=AppiumFinders)

# Core modules
CoreBroker = CommandRegistry.register("core", None, "tass.core.actions.core.core", broker=CommandBroker)

# Hooks
HookRegistry = BrokerRegistry()
# CoreHookBroker = Brokers.register("core", None, )
SeleniumHookBroker = HookRegistry.register("selenium", "core", "", broker=HookBroker)
AppiumHookBroker = HookRegistry.register("appium", "selenium", "", broker=HookBroker)