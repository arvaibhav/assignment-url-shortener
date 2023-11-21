.
|-- .env.development
|-- Dockerfile
|-- docker-compose.yaml
|-- requirements.txt
|-- run_docker.sh
|-- scripts
|   `-- mongo_models_migrations.py
`-- src
    |-- api
    |   |-- __init__.py
    |   |-- auth
    |   |   |-- __init__.py
    |   |   `-- router.py
    |   |-- common
    |   |   |-- __init__.py
    |   |   |-- authentication.py
    |   |   |-- logger.py
    |   |   `-- middlewares.py
    |   |-- router.py
    |   |-- url_shortener
    |   |   |-- __init__.py
    |   |   `-- router.py
    |   `-- user
    |       |-- __init__.py
    |       `-- router.py
    |-- config.py
    |-- core
    |   |-- __init__.py
    |   |-- counter.py
    |   `-- user_auth.py
    |-- dao
    |   |-- __init__.py
    |   |-- auth.py
    |   |-- counter.py
    |   |-- shorten_url.py
    |   `-- user.py
    |-- db
    |   |-- __init__.py
    |   |-- connection.py
    |   `-- models
    |       |-- __init__.py
    |       |-- auth.py
    |       |-- base.py
    |       |-- counter.py
    |       |-- shorten_url.py
    |       `-- user.py
    |-- main.py
    |-- schema
    |   |-- __init__.py
    |   |-- auth.py
    |   |-- url_shortner.py
    |   `-- user.py
    `-- utils
        |-- __init__.py
        |-- jwt_auth.py
        `-- string_hasher.py

14 directories, 43 files
