#!/bin/bash
  
for ((i=1; i<=5; i++))
do
    for ((j=1; j<=10; j++))
    do
        ffmpeg -i ${i}_${j}.MP4 -vf select='eq(pict_type\,I)' -vsync 2 -s 720x1280 -f image2 images/user${i}_${j}/core-%02d.jpeg
    done
done
