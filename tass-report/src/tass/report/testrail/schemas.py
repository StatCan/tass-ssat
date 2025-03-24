TESTRAIL_1_0_0 = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "title": "Testrail Report Template",
    "description": "Describes how to submit a testrail report.",
    "type": "object",
    "properties": {
        "schema-version": {
            "type": "string",
            "pattern": "^(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$"
        },
        "_type": {
            "type": "string",
            "const": "testrail",
            "description": "The type of reporter."
        },
        "package": {
            "type":"string",
            "description": "The package string to import the reporter from. Optional, for using custom reporter.",
            "pattern": "^[a-zA-Z]\\w+$|^[a-zA-Z]\\w+(\\.[a-zA-Z]\\w+)+$"
        },
        "class_name": {
            "type": "string",
            "description": "The name of the reporter class to use. Optional, for using custom reporters.",
            "pattern": "^[a-zA-Z]\\w+$"
        },
        "project_id": {
            "type": "string",
            "pattern": "\\A\\d+$\\Z",
            "description": "The TestRail project id to push reports to."
        },
        "connection": {
            "$ref": "#/$defs/conn"
        },
        "config": {
            "$ref": "#/$defs/conf"
        },
        "Cases": {
            "type": "array",
            "items": {"$ref": "#/$defs/test-case"}
        },
        "Runs": {
            "type": "array",
            "items": {"$ref": "#/$defs/test-run"}
        },
        "Plans": {
            "type": "array",
            "items": {"$ref": "#/$defs/test-plan"},
            "description": "Plans are optional"
        }
    },
    "required": ["_type", "project_id", "connection", "Cases", "Runs"],
    "$defs": {
        "conn": {
            "type": "object",
            "description": "Settings to estabish a connection through the Testrail api.",
            "properties": {
                "user": {
                    "type": "string",
                    "description": "The username for testrail credentials. If not provided user will be prompted. If value is '~' OS credentials will  be used."
                },
                "password": {
                    "type": "string",
                    "description": "The password for testrail credentials. Provided as an option, but not recommended for general use due to password safety."
                },
                "host": {
                    "type": "string",
                    "description": "Address for the server of the user credentials. Used when connecting to the api."
                },
                "ssl-verify": {
                    "type": ["string", "integer"],
                    "enum": [1, 2, 3, "1", "2", "3"],
                    "description": "Sets the ssl verification mode. 1=(default)Standard verification, 2=(WIP)Use provided certificate to verify, 3=No verify"
                },
                "url-base":{
                    "type": "string",
                    "description": "The base url to access the testrail api."
                }
            },
            "required": ["url-base"]
        },
        "conf": {
            "type": "object",
            "properties": {
                "always-close-runs": {
                    "type": "boolean",
                    "description": "Setting that determines whether all test runs are closed immediately."
                },
                "close-successful-runs": {
                    "type": "boolean",
                    "description": "Setting that determines whether successful test runs are closed."
                }
            }
        },
        "test-case":{
            "description": "Mappings for a TASS case to convert to a  Testrail case",
            "type": "object",
            "properties": {
                 "tuuid": {
                    "description": "TASS uuid of the specific case.",
                    "type": "string"
                 },
                 "id": {
                    "description": "The case ID of the case in Testrail.",
                    "type": "string",
                    "pattern": "\\A\\d+$\\Z"
                 }
            }
        },
        "test-run": {
            "description": "Mappings and description to prepare a TestRail run.",
            "type": "object",
            "properties": {
                 "cases": {
                    "description": "Cases should be either 'true' if all cases should be included, or an array containing a list of cases to include using the TASS uuid. Default is to include all cases.",
                    "type": ["array", "boolean"],
                    "items": {
                        "type": "string",
                        "pattern": "\\A\\d+$\\Z"
                    },
                    "uniqueItems": True
                 },
                 "name": {
                    "type": "string",
                    "description": "The name for the run created in Testrail. Defaults to the name of the Tass Execution file."
                 },
                 "description": {
                    "type": "string",
                    "description": "Description for the Testrail run. Defaults to use TASS details."
                 },
                 "suite_id": {
                    "type": "string",
                    "description": "The suite ID of the Testrail case if applicable",
                    "pattern": "\\A\\d+$\\Z"
                 }
            }
        },
        "test-plan": {
            "description": "Mappings and description to prepare a TestRail plan.",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name for the plan created in Testrail. Defaults to the name of the Tass Execution file."
                 },
                 "description": {
                    "type": "string",
                    "description": "Description for the Testrail plan. Defaults to use TASS details."
                 },
                 "entries": {
                    "description": "List of runs as decribed above to include in the plan.",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "\\A\\d+$\\Z"
                    }
                 }
            }
        }
    }
}