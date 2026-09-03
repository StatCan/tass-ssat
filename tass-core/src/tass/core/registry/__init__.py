from .broker import CommandBrokerRegistry

CommandBrokers = CommandBrokerRegistry()

# Selenium modules
# Selenium should contain all commands
# Selwait and selchain commands can easily be accessed via selenium
SeleniumBroker = CommandBrokers.register("selenium", "core", "tass.core.actions.browser", default_retries=1)
SeleniumWaitBroker = CommandBrokers.register("selwait", "selenium", "tass.core.actions.browser", default_retries=1)
SeleniumChainBroker = CommandBrokers.register("selchain", "selenium", "tass.core.actions.browser", default_retries=1)

# Appium modules
# appium should contain all commands
# appwait and appchain commands can easily be accessed via appium
# appium fallsback to default selenium commands
AppiumBroker = CommandBrokers.register("appium", "selenium", "tass.core.actions.mobile", default_retries=1)
AppiumWaitBroker = CommandBrokers.register("appwait", "appium", "tass.core.actions.mobile", default_retries=1)
AppiumChainBroker = CommandBrokers.register("appchain", "appium", "tass.core.actions.mobile", default_retries=1)

# Core modules
CoreBroker = CommandBrokers.register("core", None, "tass.core.actions.core")