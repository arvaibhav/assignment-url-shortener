.
|-- .env.development
|-- .gitignore
|-- Dockerfile
|-- README.md
|-- assignment_requirement_doc.md
|-- docker-compose.yaml
|-- project_structure.md
|-- requirements.txt
|-- run_docker.sh
|-- src
|   |-- __pycache__
|   |   |-- config.cpython-310.pyc
|   |   `-- main.cpython-310.pyc
|   |-- api
|   |   |-- __init__.py
|   |   |-- auth
|   |   |   |-- __init__.py
|   |   |   |-- exceptions.py
|   |   |   `-- router.py
|   |   |-- common
|   |   |   |-- __init__.py
|   |   |   |-- authentication.py
|   |   |   |-- error_response.py
|   |   |   |-- exceptions.py
|   |   |   |-- http_headers.py
|   |   |   `-- middlewares.py
|   |   |-- router.py
|   |   |-- url_shortener
|   |   |   `-- __init__.py
|   |   `-- user
|   |       |-- __init__.py
|   |       `-- router.py
|   |-- config.py
|   |-- core
|   |   |-- __init__.py
|   |   `-- user_auth.py
|   |-- dao
|   |   `-- __init__.py
|   |-- db
|   |   |-- __init__.py
|   |   |-- __pycache__
|   |   |   |-- __init__.cpython-310.pyc
|   |   |   `-- connection.cpython-310.pyc
|   |   `-- connection.py
|   |-- main.py
|   |-- schema
|   |   |-- __init__.py
|   |   |-- auth.py
|   |   `-- user.py
|   `-- utils
|       |-- __init__.py
|       |-- jwt_auth.py
|       `-- string_hasher.py
`-- temp.py

14 directories, 41 files
