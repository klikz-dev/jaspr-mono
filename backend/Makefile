-include Makefile.info

shell:
	python compile_dot_env.py && pipenv shell
build-dev-base:
	docker build . -f ../ops/docker/base-server/Dockerfile -t jaspr/base-server --build-arg BUILD_TYPE=development
build-prod-base:
	docker build . -f ../ops/docker/base-server/Dockerfile -t jaspr/base-server --build-arg BUILD_TYPE=production
build:
	docker-compose -f ../ops/docker/local.yml build
up:
	docker-compose -f ../ops/docker/local.yml up
# Only run this when `RQ_ASYNC=False`, I.E. when we're running all tasks eagerly and
# not using the scheduler.
eager-up:
	docker-compose -f ../ops/docker/local.yml up postgres redis mailhog api-server
down:
	docker-compose -f ../ops/docker/local.yml down
downv:
	docker-compose -f ../ops/docker/local.yml down -v
	rm -f fixtures_initialized
backing:
	docker-compose -f ../ops/docker/local.yml up -d postgres redis mailhog rqworker rqscheduler
minimal-backing:
	docker-compose -f ../ops/docker/local.yml up -d postgres redis mailhog
rqworker:
	docker-compose -f ../ops/docker/local.yml up rqworker
rqscheduler:
	docker-compose -f ../ops/docker/local.yml up rqscheduler
live-logs:
	docker-compose -f ../ops/docker/local.yml logs -f

addstatictoken:
	pipenv run python manage.py addstatictoken dev@jasprhealth.com
test:
	docker-compose -f ../ops/docker/local.yml run --rm api-server python manage.py test --noinput
test-keepdb:
	docker-compose -f ../ops/docker/local.yml run --rm api-server python manage.py test --noinput --keepdb
test-parallel:
	docker-compose -f ../ops/docker/local.yml run --rm api-server python manage.py test --parallel=8 --noinput
test-parallel-keepdb:
	docker-compose -f ../ops/docker/local.yml run --rm api-server python manage.py test --parallel=8 --noinput --keepdb
test-coverage:
	docker-compose -f ../ops/docker/local.yml run --rm api-server coverage run --source='jaspr' manage.py test jaspr --noinput && coverage report
test-local:
	pipenv run python manage.py test --noinput
test-local-keepdb:
	pipenv run python manage.py test --noinput --keepdb
test-local-parallel:
	pipenv run python manage.py test --parallel --noinput
test-local-parallel-keepdb:
	pipenv run python manage.py test --parallel --noinput --keepdb
test-coverage-local:
	coverage run --source='jaspr' manage.py test jaspr --noinput && coverage report && coverage html
