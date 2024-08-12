#!/bin/bash

alembic upgrade head

python app/read_db.py

python main.py 