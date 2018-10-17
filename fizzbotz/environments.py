import os

import dotenv

dotenv.load_dotenv()

DEBUG = os.getenv("FIZZBOTZ_DEBUG") is not None
DEBUG_TOKEN = os.getenv("FIZZBOTZ_DEBUG_TOKEN")
DESCRIPTION = os.getenv("FIZZBOTZ_DESCRIPTION", "A bot written by Fission#1337")
PREFIX = os.getenv("FIZZBOTZ_PREFIX", "!")
STATUS = os.getenv("FIZZBOTZ_STATUS", f"{PREFIX}help for usage")
TOKEN = os.getenv("FIZZBOTZ_TOKEN")
