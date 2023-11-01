#!/bin/bash
DATASET="ohio"
MODE="valid"

DIR="outputs/thing-$DATASET-$MODE"
mkdir $DIR

# something like this
#python main.py --dataset=$DATASET --mode=$MODE -- 2>&1 $DIR/output-gunk.txt
python main.py --dataset=$DATASET --mode=$MODE > $DIR/output-gunk.txt

mv plots/something.png $DIR