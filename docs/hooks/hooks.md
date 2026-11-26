# TASS Hooks
## What are hooks?

Hooks are code segments that can be executed at various pre-defined points during execution. As of the current version of TASS
only TASS supported hooks are available. In future updates, custom hooks can be created using the Hooks and Actions API of TASS.
Hooks must be registered in the TASS job file JSON to be executed, by using a combination of hooks and timings users can reduce setup and tear down steps
in their test cases as well as apply conditional hooks such as "on failures".

For example, the TASS "screenshot" hook can be executed at various stages of the test case, including after the test finishes, when there is an assertion failure,
or when a test case is succesful. This allows users to create test cases that will automatically take screenshots of the element being testeed or the entire viewport
without need to be explicitly defined as an action. This is useful for recording failures and succes messages without having to duplicate the step in every test case.

## TASS Hooks
### Selenium
[screenshot](./selenium.md#screenshot)