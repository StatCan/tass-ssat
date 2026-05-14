# Core TASS Actions
## Core Actions
### Usage

`core,{command}`

### Parameters

|Action|-|key|value|config_path|new_value|stored_filter<sup>2</sup>|source|value_key|wait_time|unit|\*\*secret<sup>1 2</sup>|
|------|-|:-:|:---:|:---------:|:-------:|:-----------------------:|:----:|:-------:|:-------:|:--:|:----------------------:|
|wait|-|n|n|n|n|n|n|n|y|o|n|
|store_secret_value|-|y|n|n|n|o|n|y|n|n|o|
|save_data_source|-|n|n|n|n|n|y|n|n|n|n|
|update_data_entry|-|y|n|n|y|o|n|n|n|n|o|
|add_data_source|-|n|n|y|n|n|n|n|n|n|n|
|read_value|-|y|n|n|n|n|n|n|n|n|n|
|store_value|-|y|y|n|n|n|n|n|n|n|n|

<sup>1</sup> secret is a place holder for a single use stored filter, it will accept any number of parameters that will be applied to a data source to filter it. These parameters should be applied directly, and not wrapped in a dictionary or other data structure.  

<sup>2</sup> stored_filter and \*\*secret are mutually exclusive, the value of stored_filter takes priority.