#!/bin/sh
# echo "First arg: $1"

export BASE_DIR=$(pwd)

#echo $BASE_DIR

python $BASE_DIR/src/app.py
