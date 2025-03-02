#!/bin/sh
# echo "First arg: $1"

export BASE_DIR=$(pwd)

#echo $BASE_DIR
#echo "Running Banking App ..."

python $BASE_DIR/src/app.py

#echo "Stop Banking App ..."
