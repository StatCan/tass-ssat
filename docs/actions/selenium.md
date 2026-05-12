# Selenium TASS Actions
## Basic Actions
### Usage
`selenium,{command}`
WIP

### Parameters

y - Required parameter  
n - Not Applicable  
o - Optional parameter

|Action|-|locator|page|locator_args|text|text_key|using|value|url|url_key|use_local|relative_path|name|attribute|frame|title|handle|page_id|soft|
|------|-|:-----:|:--:|:----------:|:--:|:------:|:---:|:---:|:-:|:-----:|:-------:|:-----------:|:--:|:-------:|:---:|:---:|:----:|:-----:|:--:|
|click|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|
|write|-|y|o|o|y|n|n|n|n|n|n|n|n|n|n|n|n|n|n|
|write_stored_value|-|y|o|o|n|y|n|n|n|n|n|n|n|n|n|n|n|n|n|
|select_dropdown|-|y|o|o|n|n|y|y|n|n|n|n|n|n|n|n|n|n|n|
|clear|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|
|load_url|-|n|n|n|n|n|n|n|y|n|n|n|n|n|n|n|n|n|n|
|load_file|-|n|n|n|n|n|n|n|n|n|n|y|n|n|n|n|n|n|n|
|load_page|-|n|y|n|n|n|n|n|n|o|o|n|n|n|n|n|n|n|n|
|screenshot|-|o|n|o|n|n|n|n|n|n|n|n|o|n|n|n|n|n|n|
|read_attribute|-|y|o|o|n|n|n|n|n|n|n|n|n|y|n|n|n|n|n|
|read_css|-|y|o|o|n|n|n|n|n|n|n|n|n|y|n|n|n|n|n|
|switch_frame|-|n|o|n|n|n|n|n|n|n|n|n|n|n|y|n|n|n|n|
|switch_window|-|n|o<sup>1</sup>|n|n|n|n|n|n|n|n|n|n|n|n|y<sup>1</sup>|n|n|n|
|handle_alert|-|n|n|n|o|n|n|n|n|n|n|n|n|n|n|n|o|n|n|

|assert_page_is_open|-|n|y|n|n|n|n|n|n|n|n|n|n|n|n|n|n|o|o|
|assert_alert_displayed|-|n|n|n|o|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_displayed|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_not_displayed|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_contains_text|-|y|o|o|y|n|n|n|n|n|n|n|n|n|n|n|n|n|o|

## Wait Action
### Usage

`selwait,{command}`

### Parameters
For each Wait command with a secondary command, refer to the above for additional parameters.

|Action|-|locator|page|locator_args|second_action|
|------|-|:-----:|:--:|:----------:|:-----------:|
|wait_element_clickable|-|y|o|o|o|
|wait_element_visible|-|y|o|o|o|

## Action Chain Actions
### Usage

`selchain,{command}`
### Parameters

|Action|-|locator|page|locator_args|text|offset|target|delta|
|------|-|:-----:|:--:|:----------:|:--:|:----:|:----:|:---:|