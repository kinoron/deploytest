from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods'],
    #     num_demo_participants=3,
    # ),
    dict(
        name = 'prempexp',
        app_sequence=['prempexp'],
        num_demo_participants=4,
    ),
    dict(
        name = 'prempexp_livepage',
        app_sequence=['prempexp_introduction',
                      'prempexp_livepage'],
        num_demo_participants=6,
        # use_browser_bots = True,
        # exp_cond = 1, 
        # doc="0はb=２.8, 1はb=1.4, デフォルトは1とする"
    ),
    dict(
        name = 'mpexp_livepage',
        app_sequence=[#'mpexp_introduction',
                      'mpexp_livepage',
                      'mpexp_demographic'
                      ],
        num_demo_participants=6,
    ),
    # {
    #     'name': 'svo',
    #     'display_name': "Social Value Orientation",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['svo'],
    #     'matching': 'RING',
    #     'select_items': 'FULL',
    #     'items_in_random_order': False,
    #     'scale': 0.1 ,
    #     'slider_init': 'LEFT',
    #     'random_payoff': 'RAND',
    #     'precision': 'INTEGERS',
    #     'doc': """
    #     Edit the 'matching' parameter to select RING matching or 
    #     RANDOM_DICTATOR matching.</br>
    #     Edit the 'select_items' parameter to whether we use the first six items 
    #     to calculate the payoff (PRIMARY) or the 15 items (FULL).</br>
    #     Edit the 'scale' parameter to scale the slider values.</br>
    #     Edit the 'slider_init' parameter with LEFT, RIGHT, RAND or AVG to initialize the slider.</br>
    #     Edit the 'random_payoff' parameter with RAND or SUM to determine the way to calculate the payoff.</br>
    #     Edit the 'precision' parameter with TWO_DIGITS_AFTER_POINT or INTEGERS.
    #     """
    # },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=2500, doc=""
)

PARTICIPANT_FIELDS = ['cumulative_payoff']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'ohtsubolab'
AUTH_LEVEL = 'STUDY'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7113264272484'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ['otree']

