"""
config.py

Defines dataclass schemas for application configuration and loads
values from config.json at runtime. All tunable constants live in
config.json — this module only defines shapes and provides the
load_config() entry point.
"""

# STANDARD LIBRARY IMPORTS
from dataclasses import dataclass
import json

# CLASSES
@dataclass
class LoginConfig:
    username_field: str
    password_field: str
    submit_login_button: str

@dataclass
class SearchConfig:
    exclude_attorneys_checkbox: str
    exclude_judges_checkbox: str
    last_name_field: str
    first_name_field: str
    dob_field: str
    search_button: str
    no_results_popup_message: str

@dataclass
class ResultsConfig:
    view_selection_button: str

@dataclass
class NavigationConfig:
    back_button_from_pdf_page: str
    back_button_from_selection_page: str
    reset_button: str

@dataclass
class BrowserConfig:
    login: LoginConfig
    search: SearchConfig
    results: ResultsConfig
    navigation: NavigationConfig

@dataclass
class AppConfig:
    browser: BrowserConfig

#FUNCTIONS
def load_config(json_file: str) -> AppConfig:
    """
    parse the the json file into a python dictionary, pull each sub-sections
    as the key and the strings as the values

    Args:
        json_file: path to json file

    Returns:
        returns a fully populated AppConfig object

    Example:
        config = load_config("config.json")
        config.browser.login.username_field  # "loginForm:username"
    """
    with open(json_file, "r") as json_data:
        data = json.load(json_data)

    pass
