# Appium TASS Actions
## Basic Actions
### Usage
`appium,{command}`  
Appium uses the same commands as the Selenium module, with the following additional parameters.

### Parameters

All parameters from Selenium module apply, in addition the `hide_keyboard`, the `strategy` and other associated parameters are exposed to allow testers to automatically close the soft keyboard before interacting with an element. `hide_keyboard` is a boolean value to set whether the soft keyboard should be closed before interacting with a page or not while `strategy` determines the method used to close the keyboardm generally this can be ommitted and the default strategy can be used. Depending on the strategy used, additional parameters may be required to customize behaviour (Not implemented at this time. Only default behaviour may be used.)

## Wait Actions
### Usage
`appwait,{command}`  
Appium uses the same commands as the Selenium module, with the following additional parameters.

### Parameters

Same as above.

## ActionChain Actions

ActionChains for Appium testing is not fully implemented. It may be used at own risk using the same implementation as Selenium ActionChains. Behaviour across all mobile devices is not guaranteed.