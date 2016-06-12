#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

exec /usr/bin/python `dirname $0`/manage.py "$@"
