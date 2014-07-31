#!/bin/bash

#dir=/home/akito/Desktop/Audio
dir=/var/www-lucerne/LocativeSoundShare/client/upload
#dir=/home/dnunez/upload
#inotifywait -mrq -e CREATE --format %w%f /tmp/mytest/ | while read FILE; do chmod g=u "$FILE"; done
#inotifywait -mrq -e CREATE --format %w%f /tmp/mytest/ | while IFS= read -r FILE; do chmod g=u "$FILE"; done

inotifywait -m --format '%w%f' -e create -e moved_to "$dir" |
    while read file; do
     
	echo "$file"
    	chmod g=u "$file"    
	#/var/www-lucerne/LocativeSoundShare/server/ConvertAudio.sh $file
        /home/dnunez/lucerne_support/scripts/process_upload_file.py $file
    done
