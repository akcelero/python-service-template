set quiet := true
set dotenv-load := true
set export := true
set unstable := true

# ------------------------------ UTILS ------------------------------

_default:
    just --choose

[doc("prints this list")]
[group("help")]
help:
    just --list

# ------------------------------ DOCKER ------------------------------

[confirm]
[doc("build and force-recreate up all")]
[group("docker")]
build:
    docker compose build
    docker compose up --force-recreate -d

[doc("run app in background")]
[group("docker")]
up:
    docker compose up --force-recreate -d

[doc("follow app logs")]
[group("docker")]
logs:
    docker compose logs -f

[doc("up and follow logs of app")]
[group("docker")]
upl: up logs

[doc("down everything")]
[group("docker")]
down:
    docker compose down

[doc("run bash in app container")]
[group("docker")]
bash:
    docker compose run --rm -it app bash

[doc("run tests in container")]
[group("docker")]
[group("tests")]
docker-test:
    docker compose run --rm -it app pytest

# ------------------------------ MIGRATIONS ------------------------------

[group("migrations")]
create_migration name:
    docker compose run --rm -it app alembic revision --autogenerate -m "{{ name }}"

[group("migrations")]
migrate:
    docker compose run --rm -it app alembic upgrade head

[group("migrations")]
undo_last_migration:
    docker compose run --rm -it app alembic downgrade -1

# ------------------------------ REQUIREMENTS ------------------------------

[doc("update all requirements not listed in pyproject.toml")]
[group("requirements")]
refresh_requirements:
    rm uv.lock
    uv lock

# ------------------------------ PRE-COMMIT ------------------------------

[group("pre-commit")]
install_pre_commit_hooks:
    pre-commit install

[group("pre-commit")]
update_pre_commit_hooks:
    pre-commit autoupdate

[group("pre-commit")]
run_pre_commit:
    pre-commit run --all-files --show-diff-on-failure

# ------------------------------ TESTS ------------------------------

[doc("run pytest")]
[group("tests")]
pytest *args:
    uv run pytest {{ args }}

[doc("run bandit")]
[group("tests")]
bandit:
    uv run bandit -c pyproject.toml -r src tests

[doc("run mypy")]
[group("tests")]
mypy:
    uv run mypy .

[doc("run all tests")]
[group("tests")]
test: pytest bandit mypy
