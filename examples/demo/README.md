# DEMO

## Description

This folder contains demos for the selenium-based automation using the TASS framework.

### simple_demo

A basic demo that executes the most basic selenium function against dummy-html pages that can be found in the 
`examples/demo-html` folder. This test will click several buttons, enter text into an input field and utilize the optional `wait_until` 
functions of the TASS framework. Each test case contains tests that are designed to fail for demonstration purposes using both firefox and chrome with various configurations. 
These sample tests do not use any of the additional features offered with the TASS framework, including but not limited to 
Testrail integration, TASS secrets, etc.

#### Running this DEMO

To execute this demo use the following command from your working directory replacing the '<>' with the appropriate values: `python -m tass.base --file/-f <path/to/file>/simple_demo.json --browser/-b <browser>`