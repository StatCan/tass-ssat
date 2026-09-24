from .broker import CommandBrokerRegistry, CommandBroker, SeleniumCommandBroker, FinderBroker as FBroker


CommandBrokers = CommandBrokerRegistry()
SeleniumFinders = FBroker("tass.core.actions.locate.selenium_locate")
AppiumFinders = FBroker("tass.core.actions.locate.appium_locate")

# Selenium modules
# Selenium should contain all commands
# Selwait and selchain commands can easily be accessed via selenium
SeleniumBroker = CommandBrokers.register("selenium", "core", "tass.core.actions.browser.selenium", broker=SeleniumCommandBroker, default_retries=1, finder=SeleniumFinders)
SeleniumWaitBroker = CommandBrokers.register("selwait", "selenium", "tass.core.actions.browser.selenium_wait", broker=SeleniumCommandBroker, finder=SeleniumFinders)
SeleniumChainBroker = CommandBrokers.register("selchain", "selenium", "tass.core.actions.browser.selenium_chain", broker=SeleniumCommandBroker, finder=SeleniumFinders)

# Appium modules
# appium should contain all commands
# appwait and appchain commands can easily be accessed via appium
# appium fallsback to default selenium commands
AppiumBroker = CommandBrokers.register("appium", "selenium", "tass.core.actions.mobile.appium", broker=SeleniumCommandBroker, default_retries=1, finder=AppiumFinders)
AppiumWaitBroker = CommandBrokers.register("appwait", "appium", "tass.core.actions.mobile.appium_wait", broker=SeleniumCommandBroker, finder=AppiumFinders)
AppiumChainBroker = CommandBrokers.register("appchain", "appium", "tass.core.actions.mobile.appium_chain", broker=SeleniumCommandBroker, finder=AppiumFinders)

# Core modules
CoreBroker = CommandBrokers.register("core", None, "tass.core.actions.core.core", broker=CommandBroker)