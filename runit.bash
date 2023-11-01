#!/bin/bash
DATASET="ohio"
SUBJECT="559"
MODEL="base"
PHS=("60" "120")
EXP="test_bash"
PARAMS="base"
MODE="test"
PLOT="1"

# something like this
#python main.py --dataset=$DATASET --mode=$MODE -- 2>&1 $DIR/output-gunk.txt
for PH in "60" "120"; do 
echo $PH
DIR="outputs/$MODEL/$EXP/ph-$PH"
mkdir -p $DIR
python main.py --dataset=$DATASET --subject=$SUBJECT --model=$MODEL --params=$PARAMS --ph=$PH --exp=$EXP --mode=$MODE --plot=$PLOT > $DIR/$DATASET$()_$SUBJECT.txt
done