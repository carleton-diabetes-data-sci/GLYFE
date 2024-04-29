#!/bin/bash

dir_path="data/sap100"  # replace with your directory path

for file in "$dir_path"/*; do
  filename=$(basename "$file")
  # add in logic to see if the name has already been changed
  short_name=${filename:21:4}
#   echo $short_name
  mv "$file" "$dir_path/$short_name.csv"
done