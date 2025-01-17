from os import environ

SESSION_CONFIGS = [
    dict(
        name='FSE_horserace',
        display_name="FSE_horserace",
        app_sequence=['binary_choices'],
        num_demo_participants=3,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, 
    participation_fee=3.0, 
    doc=""
)

ROOMS = [
    dict(
        name='FSE_test',
        display_name='FSE_test',
    ),
    dict(
        name='FSE_test_prolific',
        display_name='FSE_test_prolific',
    ),
    dict(
        name='bisection_test_prolific',
        display_name='bisection_test_prolific',
    ),
    dict(
        name='Prolific',
        display_name='Prolific',
        # participant_label_file='_rooms/binary_choices.txt',
        # use_secure_urls=True,
    ),
]

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '9162759776912'

INSTALLED_APPS = ['otree']
