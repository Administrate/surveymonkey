from surveymonkey.responses.validators import is_valid_surveymonkey_url


RESPONSE_SCHEMA = {
    "id": {
        "type": "string",
        "required": True
    },
    "collector_id": {
        "type": "string",
        "required": True
    },
    "survey_id": {
        "type": "string",
        "required": True
    },
    "analyze_url": {
        "type": "string",
        "validator": is_valid_surveymonkey_url,
        "required": True
    },
    "edit_url": {
        "type": "string",
        "validator": is_valid_surveymonkey_url,
        "required": True
    },
    "href": {
        "type": "string",
        "validator": is_valid_surveymonkey_url,
        "required": True
    },
    "ip_address": {
        "type": "string",
        "required": True
    },
    "date_created": {
        "type": "datetime",
        "required": True
    },
    "date_modified": {
        "type": "datetime",
        "required": True
    },
    "collection_mode": {
        "type": "string",
        "allowed": ["default", "preview", "data_entry", "survey_preview", "edit"],
        "required": True
    },
    "response_status": {
        "type": "string",
        "allowed": ["completed", "partial", "overquota", "disqualified"],
        "required": True
    },
    "pages": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
                "id": {
                    "type": "string",
                    "required": True
                },
                "questions": {
                    "type": "list",
                    "required": True,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "id": {
                                "type": "string",
                                "required": True
                            },
                            "variable_id": {
                                "type": "string",
                                "required": False
                            },
                            "answers": {
                                "type": "list",
                                "required": True,
                                "schema": {
                                    "type": "dict",
                                    "required": True,
                                    'anyof': [
                                        {
                                            "allow_unknown": False,
                                            "schema": {}  # Answer can be an empty dict
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "other_id": {
                                                    "type": "string",
                                                    "dependencies": ["text"],
                                                    "required": True,
                                                },
                                                "text": {
                                                    "type": "string",
                                                    "required": True
                                                }
                                            }
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "col_id": {
                                                    "type": "string",
                                                    "required": True,
                                                },
                                                "choice_id": {
                                                    "type": "string",
                                                    "required": True,
                                                },
                                                "row_id": {
                                                    "type": "string",
                                                    "required": True,
                                                }
                                            }
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "choice_id": {
                                                    "type": "string",
                                                    "required": True
                                                }
                                            }
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "choice_id": {
                                                    "type": "string",
                                                    "required": True
                                                },
                                                "row_id": {
                                                    "type": "string",
                                                    "required": True,
                                                },
                                            }
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "text": {
                                                    "type": "string",
                                                    "required": True
                                                }
                                            }
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "text": {
                                                    "type": "string",
                                                    "required": True
                                                },
                                                "row_id": {
                                                    "type": "string",
                                                    "required": True,
                                                },
                                            }
                                        },
                                        {
                                            "allow_unknown": False,
                                            "schema": {
                                                "text": {
                                                    "type": "string",
                                                    "required": True
                                                },
                                                "content_type": {
                                                    "type": "string",
                                                    "required": True,
                                                },
                                            }
                                        },
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
