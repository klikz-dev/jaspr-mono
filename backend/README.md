# Jaspr Backend Documentation

### Local Django With Backing Docker Services

#### Installation, Building, and Setup Before Building
- Install Docker (preferably the latest version).
- Make sure the Docker daemon is running.

#### Setup Before Running
- Get a copy of the .env.local environment file from another developer on the team and place it in the backend folder.
- Run `python compile_dot_env.py`.  This will merge your local environment variables with the service specific environment variables from the ops project.
- Install the latest version of pipenv on your computer
- Run `pipenv install` and `pipenv install --dev` in the backend folder
- You should now be able to run the project

#### Setup Database
- Make sure you are within the pipenv environment by running `pipenv shell`.
- Install migrations by running `python manage.py migrate`
- Load default fixture data by running the following commands:
  ```shell
  python manage.py load_fixtures media
  python manage.py load_fixtures content
  python manage.py load_fixtures user
  python manage.py load_fixtures dev_only
  ```

#### Running
- Run `make minimal-backing` which will boot up all the necessary backing services for the local Django application.
- Run `python manage.py runserver 8014`.

#### Tests
- From within pipenv shell you'll need to set the test environment variables.  You can do that by running these commands from your shell:
  ```shell
  export DJANGO_SETTINGS_MODULE=jaspr.settings.test
  ```
  or on Windows
  ```shell
  set DJANGO_SETTINGS_MODULE=jaspr.settings.test
  ```
- Run `python manage.py test`
  - Note, there are lots of flags that can help you speed up tests, such as `--parallel 8` or `--keepdb`.  You can view them by running `python manage.py test --help`
- Before running the app again, you may need to set your environment back to the local environment
  ```shell
  export DJANGO_SETTINGS_MODULE=jaspr.settings.local
  ```

### Notes
- `.env.local` is only read when `READ_ENV_LOCAL_FILE=True` (which is `False` by default when running dockerized Django). Hence, any environment customizations you want to make just for local Django can be put in `.env.local`. Those values also take precedence and override any of the files in `.envs/.local/` (which are read in by local Django because we set `ENV_FILES_FOLDER_TO_READ=.local` in `.env.local`).
- MacOSX can have an issue with psycopg2. ld: library not found for -lssl  see solution here: https://stackoverflow.com/a/60313038

## Setting Up Pre Commit (with Black Formatting)
Run `pre-commit install` once you've done the above, and then all the pre-commit hooks will run every time you try and commit. If any of them do not pass (I.E. if `black` reformats your code or there are debug statements present), make sure to check which once didn't pass. If it's just `black`, then add all the files that black modified and commit again with the same commit message. If it's a different hook, there may be debug statements or errors in the code that need to be fixed before committing.


## Flushing Redis Queues
If you ever want/need to clear all of the redis queues, a management command is provided that will remove all of the redis data and results. As of the time of writing, this essentially gives a clean slate for all of the in memory redis state. The command to run is:

`./manage.py flush_redis_queues`


## Other Redis Notes
At the time of writing, when a job fails because of an unhandled exception, it is moved into the failed job registry. Currently, failed jobs are removed after eight days if they were queued from `jaspr.apps.common.jobs.rq.enqueue`, and a year otherwise (I.E. if a scheduled job executes and fails).

A management command is provided (mostly for production usage, but could also be helpful on other servers) for removing failed jobs that have been sitting in the failed registry for longer than a certain amount of time. Here is a usage example:

`./manage.py delete_failed_jobs --high 48 --default 24 --low 30`

This would cause all failed jobs from `high` to be deleted if they are older than 48 hours, `default` to be deleted if they are older than 24 hours, and `low` to be deleted if they are older than 30 hours. If the optional arguments for number of hours aren't provided, 24 hours is the current default.


## Notes For Upgrading Django
Anytime there is a piece of code that relies on private internals of Django, it is
recommended to put a comment that contains `!INSPECT_WHEN_UPGRADING_DJANGO!`, as
it would be easy to search for when upgrading Django, especially for a major
upgrade.

https://bitbucket.org/ebpi/jaspr-mono/src/update-documentation/backend/
