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
    try:
        with open(json_file, "r") as json_data:
            data = json.load(json_data)

        browser_data = data["Browser"]

        login_data = browser_data["Login"]
        search_data = browser_data["Search"]
        results_data = browser_data["Results"]
        navigation_data = browser_data["Navigation"]

        login_config = LoginConfig(
            username_field=login_data["username_field"],
            password_field=login_data["password_field"],
            submit_login_button=login_data["submit_login_button"],
        )

        search_config = SearchConfig(
            exclude_attorneys_checkbox=search_data["exclude_attorneys_checkbox"],
            exclude_judges_checkbox=search_data["exclude_judges_checkbox"],
            last_name_field=search_data["last_name_field"],
            first_name_field=search_data["first_name_field"],
            dob_field=search_data["dob_field"],
            search_button=search_data["search_button"],
            no_results_popup_message=search_data["no_results_popup_message"],
        )

        results_config = ResultsConfig(
            view_selection_button=results_data["view_selection_button"],
        )

        navigation_config = NavigationConfig(
            back_button_from_pdf_page=navigation_data["back_button_from_pdf_page"],
            back_button_from_selection_page=navigation_data["back_button_from_selection_page"],
            reset_button=navigation_data["reset_button"],
        )

        browser_config = BrowserConfig(
            login=login_config,
            search=search_config,
            results=results_config,
            navigation=navigation_config
        )

        app_config = AppConfig(browser=browser_config)
        return app_config
    except FileNotFoundError:
        raise FileNotFoundError(f"config file not found: {json_file}")
    except KeyError as e:
        raise KeyError(f"Missing key in config.json: {e}")