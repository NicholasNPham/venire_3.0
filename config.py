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
class SecondsConfig:
    pause_between_actions: int
    webdriver_wait_timeout: int
    no_results_wait_timeout: int

@dataclass
class BrowserConfig:
    login: LoginConfig
    search: SearchConfig
    results: ResultsConfig
    navigation: NavigationConfig
    seconds: SecondsConfig

@dataclass
class AppConfig:
    """
    Configuration loaded from the 'App' section of config.json.

    Holds outcome label strings written to Excel and the target workbook filename.
    These values are set in config.json so they can be changed without touching source code.

    Attributes:
        outcome_no_results: Written to Excel when the search returns no matches.
        outcome_complete:   Written to Excel when a CH record is found.
        outcome_error:      Written to Excel when an unexpected error occurs.
        outcome_bad_format: Written to Excel when a row could not be parsed correctly.
        excel_file:         Filename of the Excel workbook to read and update.

    Example:
        config = load_config("config.json")
        config.app.outcome_complete  # "CH Found"
    """
    outcome_no_results: str
    outcome_complete: str
    outcome_error: str
    outcome_bad_format: str
    excel_file: str

@dataclass
class RootConfig:
    """
    Top-level configuration object returned by load_config().

    Holds all configuration sections for the application.

    Attributes:
        browser: All browser/Selenium related configuration.
        app:     Application-level outcome labels and filenames.

    Example:
        config = load_config("config.json")
        config.browser.seconds.webdriver_wait_timeout  # 5
        config.app.excel_file                          # "VENIRE.xlsx"
    """
    browser: BrowserConfig
    app: AppConfig

#FUNCTIONS
def load_config(json_file: str) -> RootConfig:
    """
    Loads and parses config.json into a fully populated RootConfig object.

    Args:
        json_file: Path to the JSON configuration file.

    Returns:
        A RootConfig instance containing all browser and app configuration.

    Example:
        config = load_config("config.json")
        config.browser.login.username_field  # "loginForm:username"
        config.app.outcome_complete          # "CH Found"
        config.app.excel_file                # "VENIRE.xlsx"
    """
    try:
        with open(json_file, "r") as json_data:
            data = json.load(json_data)

        browser_data = data["Browser"]
        app_data = data["App"]

        login_data = browser_data["Login"]
        search_data = browser_data["Search"]
        results_data = browser_data["Results"]
        navigation_data = browser_data["Navigation"]
        seconds_data = browser_data["Seconds"]

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

        seconds_config = SecondsConfig(
            pause_between_actions=seconds_data["pause_between_actions"],
            webdriver_wait_timeout=seconds_data["webdriver_wait_timeout"],
            no_results_wait_timeout=seconds_data["no_results_wait_timeout"]
        )

        browser_config = BrowserConfig(
            login=login_config,
            search=search_config,
            results=results_config,
            navigation=navigation_config,
            seconds=seconds_config
        )

        app_config = AppConfig(
            outcome_no_results=app_data["outcome_no_results"],
            outcome_complete=app_data["outcome_complete"],
            outcome_error=app_data["outcome_error"],
            outcome_bad_format=app_data["outcome_bad_format"],
            excel_file=app_data["excel_file"],
        )

        root_config = RootConfig(browser=browser_config, app=app_config)
        return root_config
    except FileNotFoundError:
        raise FileNotFoundError(f"config file not found: {json_file}")
    except KeyError as e:
        raise KeyError(f"Missing key in config.json: {e}")