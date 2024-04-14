#!/bin/bash
alembic upgrade head;
alembic revision --autogenerate -m 'initial';
alembic upgrade head;
python src/main.py;