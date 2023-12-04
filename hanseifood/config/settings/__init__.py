import os
import dotenv


dotenv.load_dotenv()
SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")

if SETTINGS_MODULE == 'config.settings.prod':
    from .prod import *
elif SETTINGS_MODULE == 'config.settings.dev':
    from .dev import *
else:
    raise Exception(f"Settings not found: '{SETTINGS_MODULE}'")
