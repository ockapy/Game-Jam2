#!/bin/bash
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"

python client/main.py

PATH="$PATH"