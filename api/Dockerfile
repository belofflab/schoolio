FROM python:3.9

WORKDIR /opt/pdd

RUN python3 -m pip install virtualenv 
RUN python3 -m virtualenv /opt/pdd/venv

COPY ./pyproject.toml ./poetry.lock* /opt/pdd/

RUN /opt/pdd/venv/bin/pip install poetry

RUN /opt/pdd/venv/bin/poetry config virtualenvs.create false
RUN /opt/pdd/venv/bin/poetry install --no-dev --no-root

COPY . /opt/pdd


CMD ["/opt/pdd/venv/bin/poetry", "run", "fastapi-app"]

EXPOSE 8000