#!/bin/bash
DATASET="sap100"
SUBJECTS="85e54 0ae3c 2eff7 2e101 f0a42 fc2b1 30c42 07d80 f086c 546b3 07f02 67eaf b09b5 a71ab bee62 99399 6fe50 63676 fa6d1 16010 c3e1f e0e0c 2e63d 77526 415a5 c69a1 301e2 2868b 66dd9 e350e e0d4c 9ba04 4a594 473e2 55659 83ce9 36456 e0971 f9450 66933 ee100 80a5c 2e2a5 94d6e ced97 ed0d5 e9f83 c4995 dbcb6 b3eb8 d3e29 1fd6c dbfd8 54b09 86488 f4030 55c5e c45f5 7f174 0a1f3 6deb1 54dae fcb97 65d01 10005 5a797 9518f d4727 1ccbd db8c8 f8ac6 fefe4 9d5e8 99454 9518e b5b85 d5894 9036a 40234 ee6ff cc5ec cc74a 7e3b2 37603 24b7a 2fdfe"
PHS="30 60 120"
EXP="all_sap100"
MODE="test"
PLOT="1"

declare -A PARAMS_MODELS
# PARAMS_MODELS["ar"]="arimax"
# PARAMS_MODELS["arx"]="arimax"
# PARAMS_MODELS["base"]="base"
# PARAMS_MODELS["elm"]="elm"
# PARAMS_MODELS["ffnn"]="ffnn"
PARAMS_MODELS["gp"]="gp"
# PARAMS_MODELS["lstm"]="lstm"
# PARAMS_MODELS["poly"]="poly"
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