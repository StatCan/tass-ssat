from .registry import CommandModuleRegistry, CommandRegistry

module_registry = CommandModuleRegistry()

# Selenium modules
# Selenium should contain all commands
# Selwait and selchain commands can easily be accessed via selenium
selenium = module_registry.register("selenium", "core", "tass.core.actions.browser")
selwait = module_registry.register("selwait", "selenium", "tass.core.actions.browser")
selchain = module_registry.register("selchain", "selenium", "tass.core.actions.browser")

# Appium modules
# appium should contain all commands
# appwait and appchain commands can easily be accessed via appium
# appium fallsback to default selenium commands
appium = module_registry.register("appium", "selenium", "tass.core.actions.mobile")
appwait = module_registry.register("appwait", "appium", "tass.core.actions.mobile")
appchain = module_registry.register("appchain", "appium", "tass.core.actions.mobile")

# Core modules
core = module_registry.register("core", None, "tass.core.actions.core")