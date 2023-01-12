#!/bin/sh

for img in *
do
    if [[ $img == *.drawio ]]
    then
        imagename="${img%.*}"
        #echo "${imagename}"
        draw.io -x -f svg -o ${imagename}.svg $img
    fi
done
