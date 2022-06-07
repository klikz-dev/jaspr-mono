"""
Settings mixin for Django for local development and/or testing.

Ordering/Derivation Chart:
- root --> local_mixin
"""
from .root import *  # isort:skip  # noqa

# Environment Variables and File Handling
# ------------------------------------------------------------------------------
# Should `.env.local` be read in?
READ_ENV_LOCAL_FILE = env.bool("READ_ENV_LOCAL_FILE", default=True)
if READ_ENV_LOCAL_FILE:
    # OS environment variables take precedence over variables from .env.local, etc.
    env.read_env(str(ROOT_DIR / ".env.local"))

# Should one of the folders in `.envs/` have the files within it read in?
ENV_FILES_FOLDER_TO_READ = env("ENV_FILES_FOLDER_TO_READ", default="")
if ENV_FILES_FOLDER_TO_READ:
    # OS environment variables take precedence over variables from
    # `.envs/{ENV_FILES_FOLDER_TO_READ}`, etc.
    env.read_env(str(ROOT_DIR / f".envs/{ENV_FILES_FOLDER_TO_READ}/.django"))
    env.read_env(str(ROOT_DIR / f".envs/{ENV_FILES_FOLDER_TO_READ}/.postgres"))
    env.read_env(str(ROOT_DIR / f".envs/{ENV_FILES_FOLDER_TO_READ}/.secrets"))
    env.read_env(str(ROOT_DIR / f".envs/{ENV_FILES_FOLDER_TO_READ}/.specific"))

# NOTE: Yes, this is duplicated from above. The very top lets us use `.env.local` to
# specify `ENV_FILES_FOLDER_TO_READ`, and then we re-read this in to use `.env.local`
# take precedence over any other the other `.envs/...` files.
if READ_ENV_LOCAL_FILE and ENV_FILES_FOLDER_TO_READ:
    # OS environment variables take precedence over variables from .env.local, etc.
    env.read_env(str(ROOT_DIR / ".env.local"))
