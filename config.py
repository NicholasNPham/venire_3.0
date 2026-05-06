"""

config file

"""

from dataclasses import dataclass

@dataclass
class LoginConfig:
    # login page selectors
    pass

@dataclass
class SearchConfig:
    # search form selectors
    pass

@dataclass
class ResultsConfig:
    # results page selectors
    pass

@dataclass
class NavigationConfig:
    # back buttons, reset button
    pass

@dataclass
class BrowserConfig:
    login: LoginConfig
    search: SearchConfig
    results: ResultsConfig
    navigation: NavigationConfig