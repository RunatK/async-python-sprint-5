#!/bin/bash
alembic revision --autogenerate -m 'initial';
python src/main.py;