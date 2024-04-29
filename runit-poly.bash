#!/bin/bash
DATASET="ohio"
SUBJECTS="559 563 570"
PHS="30 60 120"
EXP="test_datalad"
MODE="test"
PLOT="1"

declare -A PARAMS_MODELS
# PARAMS_MODELS["ar"]="arimax"
# PARAMS_MODELS["arx"]="arimax"
# PARAMS_MODELS["base"]="base"
# PARAMS_MODELS["elm"]="elm"
# PARAMS_MODELS["ffnn"]="ffnn"
# PARAMS_MODELS["gp"]="gp"
# PARAMS_MODELS["lstm"]="lstm"
PARAMS_MODELS["poly"]="poly"
# PARAMS_MODELS["svr"]="svr"

for SUBJECT in $SUBJECTS; do 
    echo $SUBJECT
    
    for PH in $PHS; do 
        echo $PH

        for PARAM in ${!PARAMS_MODELS[@]}; do
            
            MODEL=${PARAMS_MODELS[$PARAM]}
            echo $PARAM
            echo $MODEL

            DIR="experiments/$EXP/outputs/$PARAM/ph-$PH"
            mkdir -p $DIR
            python main.py --dataset=$DATASET --subject=$SUBJECT --model=$MODEL --params=$PARAM --ph=$PH --exp=$EXP --mode=$MODE --plot=$PLOT > $DIR/$DATASET$()_$SUBJECT.txt
        done
    done
done