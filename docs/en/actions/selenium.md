# Selenium TASS Actions
## Basic Actions
### Usage
`selenium,{command}`
<br>For typical use, driver and find arguments are provided by the automation framework and configured by the user as part of the test. User inputted parameters are listed below.

<a id="tass-core.src.tass.core.actions.browser.selenium.click"></a>

#### click

```python
def click(driver, find=_find_element, **kwargs)
```

Click an element in the DOM

Execute the selenium click function against the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.write"></a>

#### write

```python
def write(driver, find=_find_element, text='', **kwargs)
```

Send a string to an element in the DOM

Execute the selenium send_keys(str) function against the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  text:
  The str text that is to be sent to the element. Behaviour of
  this function is determined by the properties of the
  element, as such there is no guarantee the exact string
  will be entered as is. ex: an input element that only accepts
  numbers will not accept other characters but may not raise an
  exception. Default is an empty str.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.write_stored_value"></a>

#### write\_stored\_value

```python
def write_stored_value(driver, find=_find_element, text_key='', **kwargs)
```

Send a stored string to an element in the DOM

Execute the selenium send_keys(str) function against the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  text_key:
  The str key used to store a str using ValueStore.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.select_dropdown"></a>

#### select\_dropdown

```python
def select_dropdown(driver, value, using, find=_find_element, **kwargs)
```

Select an option from a dropdown using text, value, or index in the DOM

Execute the selenium Select.select_by_* function
described by 'using' against the locator that is part of the kwargs
argument. If a WebDriverException occurs the action is attempted
a second time before allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element function.
  value:
  The DOM value to be used for selection. This can be
  the visible text (which must match the element text in
  the DOM exactly), it can be the value of the option
  element or it can be the index attribute of the desired
  option element.
  using:
  A str value that is part of the set of possible methods to
  select from a dropdown. Possible values include "text,
  value, and index" to be used to determine the
  select function from selenium.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.clear"></a>

#### clear

```python
def clear(driver, find=_find_element, **kwargs)
```

Clear the value of a text input element in the DOM

Execute the selenium clear function against the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.load_url"></a>

#### load\_url

```python
def load_url(driver, url)
```

Load the provided URL in the current browser window

Execute the selenium get function. Requires a fully formed
and formatted URL.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  url:
  The url to be loaded. Must be complete and correctly formatted.

<a id="tass-core.src.tass.core.actions.browser.selenium.load_file"></a>

#### load\_file

```python
def load_file(driver, relative_path)
```

Load the provided file in the current browser window

Execute the selenium get function. Requires a file
path relative to the root directory.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  relative_path:
  The file path to be loaded. Must be relative to the root directory.

<a id="tass-core.src.tass.core.actions.browser.selenium.load_page"></a>

#### load\_page

```python
def load_page(driver, page, url_key='url', use_local=False)
```

Load a page using the URL provided in the POM

Execute the selenium get function against the URL or
file path provided in the given page.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  page:
  The key combination for the POM page object.
  url_key:
  The key for the url in the required environment.
  in the case of multiple URLs for the same page in
  different environments. The default value is 'url'.
  The default URL for the POM object should be 'url'.
  use_local:
  A flag that indicates if a local file should be used. In which
  case the provided url is treated like a relative file path
  instead of a web URL.

<a id="tass-core.src.tass.core.actions.browser.selenium.read_attribute"></a>

#### read\_attribute

```python
def read_attribute(driver, attribute, find=_find_element, **kwargs)
```

Read the value of an attribute for an element in the DOM

Execute the selenium get_attribute function against the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  attribute:
  The str name of the attribute to be read from the element.
  Must match the HTML element attribute name exactly.
  Different browsers may use different spellings for the same
  values, at this time there is no automatic translation of
  attribute names so the exact value of the attribute name
  for the open browser must be supplied.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.read_css"></a>

#### read\_css

```python
def read_css(driver, attribute, find=_find_element, **kwargs)
```

Read the value of a css attribute for an element in the DOM

Execute the selenium value_of_css function against the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  attribute:
  The str name of the attribute to be read from the element.
  Must match the CSS element attribute name exactly.
  Different browsers may use different spellings for the same
  values, at this time there is no automatic translation of
  attribute names so the exact value of the attribute name
  for the open browser must be supplied.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.read_text"></a>

#### read\_text

```python
def read_text(driver, find=_find_element, **kwargs)
```

Read the text value for an element in the DOM

Get the text value of the element with the locator
that is part of the kwargs argument. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.switch_frame"></a>

#### switch\_frame

```python
def switch_frame(driver, frame, page=None, find=_find_element)
```

Change the active frame by name or element

Execute the selenium switch_to.frame function against the locator
provided by the frame attribute. If a WebDriverException
occurs the action is attempted a second time before
allowing the exception to be raised to the next level.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  frame:
  The frame that should take focus. This can be either a str
  name or id of the frame or it can be a dictionary composed of 'by'
  and 'value' as a locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.switch_window"></a>

#### switch\_window

```python
def switch_window(driver, title=None, page=None)
```

Change to the next tab/window or switch to one wih a matching title.

Execute the selenium switch_to.window function. If title
is not given then switch to the next tab/window, if a str title
is provided then all open windows/tabs are cycled through
until one with a matching title is found.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  title:
  The title (str) of a window or tab to be switched to.
  The title must be an exact match in order for it to be
  found and switched to correctly.

<a id="tass-core.src.tass.core.actions.browser.selenium.close"></a>

#### close

```python
def close(driver)
```

Closes the currently open browser tab or window.

Execute the selenium close function, any alerts
must be handled before continuing execution. Use
handle_alert function.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.

<a id="tass-core.src.tass.core.actions.browser.selenium.quit"></a>

#### quit

```python
def quit(driver)
```

Closes the current browser session.

Executes the Selenium quit function. By default,
will also reset all instances related to the
browser driver (waits, driver, etc.).

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.

<a id="tass-core.src.tass.core.actions.browser.selenium.handle_alert"></a>

#### handle\_alert

```python
def handle_alert(driver, handle=True, text=None)
```

Handle an expected browser alert.

Utilizing the Selenium Alert class, handle an expected
alert using the method described by handle. The soft
parameter determines behaviour if an alert is not present.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  handle:
  How to handle the alert. Options include:
  'accept', 1 or True to accept the alert
  and 'dismiss', 0, or False to dismiss the
  alert. A value of None will provide default
  behaviour of 'accept'

<a id="tass-core.src.tass.core.actions.browser.selenium.assert_alert_displayed"></a>

#### assert\_alert\_displayed

```python
def assert_alert_displayed(driver, text=None, soft=False)
```

Assert that an alert is currently displayed in the browser.

Using the Selenium Alert class, assert that an alert is currently
displayed in the browser. If no alert is present a
TassSoftAssertionError or TassHardAssertionError is raised
depending on the value of soft.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  soft:
  Boolean flag that indicates if a failed assertion
  should end execution. If True execution for the
  current test stops upon returning. If false, error is
  recorded and execution can continue. The default is False.

<a id="tass-core.src.tass.core.actions.browser.selenium.assert_page_is_open"></a>

#### assert\_page\_is\_open

```python
def assert_page_is_open(driver,
                        page=None,
                        find=_find_element,
                        soft=False,
                        page_id=None)
```

Assert the given page is open using the described method

Assert that the given page is open using one of the pre-defined methods.
'element' checks for the presence of a given element.
'title' checks for the given title.
'url' checks for the given url.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element function.
  method:
  The str representation of the desired method.
  Value must match one of the predefined methods
  given above.

<a id="tass-core.src.tass.core.actions.browser.selenium.assert_contains_text"></a>

#### assert\_contains\_text

```python
def assert_contains_text(driver,
                         text,
                         find=_find_element,
                         soft=False,
                         exact=False,
                         **kwargs)
```

Assert the given text is displayed in the element.
Can be soft, or hard check.

Using the WebElement text attribute, confirm that the specified element
contains the text fragment provided.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  text:
  The complete text or a text fragment that
  should be in the given element
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element function.

<a id="tass-core.src.tass.core.actions.browser.selenium.assert_displayed"></a>

#### assert\_displayed

```python
def assert_displayed(driver, find=_find_element, soft=False, **kwargs)
```

Assert the given element is displayed. Can be a soft or hard check

Execute the selenium is_displayed function against the locator
provided. Then return true if it is displayed.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  soft:
  Boolean flag that indicates if a failed assertion
  should end execution. If True execution for the
  current test stops upon returning. If false, error is
  recorded and execution can continue. The default is False.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.assert_not_displayed"></a>

#### assert\_not\_displayed

```python
def assert_not_displayed(driver, find=_find_element, soft=False, **kwargs)
```

Assert the given element is not displayed. Can be a soft of hard check

Execute the selenium is_displayed function against the locator
provided. Then return true if it is not displayed.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  soft:
  Boolean flag that indicates if a failed assertion
  should end execution. If True execution for the
  current test stops upon returning. If false, error is
  recorded and execution can continue. The default is False.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.

<a id="tass-core.src.tass.core.actions.browser.selenium.assert_attribute_contains_value"></a>

#### assert\_attribute\_contains\_value

```python
def assert_attribute_contains_value(driver,
                                    attribute,
                                    value,
                                    find=_find_element,
                                    soft=False,
                                    exact=False,
                                    **kwargs)
```

Assert that the given element contains the specified
value for the given attribute.

Execute the Selenium read_attribute function and compare the
actual value taken from the DOM to the given value.

**Arguments**:

  driver:
  The RemoteWebDriver object that is connected
  to the open browser.
  attribute:
  The name of the atribute to check within the DOM.
  value:
  The expected value of the above attribute within the DOM.
  find:
  The function to be called when attempting to locate
  an element. Must use either a explicit wait function
  or the default _find_element fuinction.
  soft:
  Boolean flag that indicates if a failed assertion
  should end execution. If True execution for the
  current test stops upon returning. If false, error is
  recorded and execution can continue. The default is False.
  exact:
  Flag to determine if an exact match is needed. Useful for
  checking for a partial string value. If exact is True
  the actual value must match exactly, and if exact is
  False the actual and expected and compared using the
  "in" keyword. The default is False.
  **kwargs:
  Dictionary containing additional parameters. Contents
  of the dictionary will vary based on the find function used.
  By default, _find_element is used and thus kwargs
- `requires` - locator.


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
|read_text|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|
|switch_frame|-|n|o|n|n|n|n|n|n|n|n|n|n|n|y|n|n|n|n|
|switch_window|-|n|o<sup>1</sup>|n|n|n|n|n|n|n|n|n|n|n|n|y<sup>1</sup>|n|n|n|
|handle_alert|-|n|n|n|o|n|n|n|n|n|n|n|n|n|n|n|o|n|n|
|close|-|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|
|quit|-|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|n|
|assert_page_is_open|-|n|y|n|n|n|n|n|n|n|n|n|n|n|n|n|n|o|o|
|assert_alert_displayed|-|n|n|n|o|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_displayed|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_not_displayed|-|y|o|o|n|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_contains_text|-|y|o|o|y|n|n|n|n|n|n|n|n|n|n|n|n|n|o|
|assert_attribute_contains_value|-|y|o|o|n|n|n|y|n|n|n|n|n|y|n|n|n|n|o|

<sup>1</sup> title parameter can be omitted if it is included in the POM specified by the page parameter.

## Wait Action
### Usage

`selwait,{command}`

### Parameters

For each Wait command with a secondary action, refer to the above for additional parameters. Both actions must share the same locator, page and locator_args parameters.

y - Required parameter  
n - Not Applicable  
o - Optional parameter  

|Action|-|locator|page|locator_args|second_action|
|------|-|:-----:|:--:|:----------:|:-----------:|
|wait_element_clickable|-|y|o|o|o|
|wait_element_visible|-|y|o|o|o|

## Action Chain Actions
### Usage

`selchain,{command}`  
ActionChains are built by appending a series of actions that are later executed in sequence. The perform command must be called to execute the Action Chain in TASS tests. The reset command removes all appended actions, otherwise any added commands are not removed.

### Parameters

y - Required parameter  
n - Not Applicable  
o - Optional parameter  

|Action|-|locator|page|locator_args|text|xoffset/yoffset|target|deltax/deltay|
|------|-|:-----:|:--:|:----------:|:--:|:----:|:----:|:---:|
|perform|-|n|n|n|n|n|n|n|
|reset|-|n|n|n|n|n|n|n|
|click|-|o|o|o|n|n|n|n|
|write|-|y|o|o|y|n|n|n|
|move_mouse|-|o<sup>1</sup>|o|o|n|o<sup>1</sup>|n|n|
|drag_and_drop|-|y|o|o|n|o<sup>1</sup>|o<sup>1</sup>|n|
|scroll|-|o|o|o|n|o<sup>1</sup>|n|o<sup>1</sup>|

<sup>1</sup> Default null/0 values are provided for these parameters, but without user inputed values for at least one field, no measurable effect is taken.
