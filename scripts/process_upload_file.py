#!/usr/bin/python

"""process_upload_file.py: Converts images."""
# Requires:
# sudo apt-get install libogg-dev libvorbis-dev lame libfaad2
# cd ~;wget https://bootstrap.pypa.io/get-pip.py; sudo python get-pip.py
# pip install pillow  # For Image processing
# sudo apt-get install ubuntu-restricted-extras 

import os,sys,itertools, subprocess
from PIL import Image

__author__ = "David Nunez"
__email__  = "dnunez@media.mit.edu"

OUTPUT_IMG_FOLDER_ORIGINAL = "/home/dnunez/upload/img/feed/"
OUTPUT_IMG_FOLDER_RESIZED = "/home/dnunez/upload/img/feed/"
OUTPUT_IMG_FOLDER_THUMBNAIL = "/home/dnunez/upload/img/feed/"

ORIGINAL_IMG_FILENAME_SUFFIX = ""
RESIZED_IMG_FILENAME_SUFFIX = "_resized"
THUMBNAIL_IMG_FILENAME_SUFFIX = "_thumbnail"

MP3_FOLDER = "/home/dnunez/upload/snd/mp3/"
OGG_FOLDER = "/home/dnunez/upload/snd/ogg/"


def alternative_names(filename):
    yield filename
    base, ext = os.path.splitext(filename)
    yield base + "_1" + ext
    for i in itertools.count(1):
        yield base + "_%i" % i + ext

def main(argv):
    for filename in argv:
        try:
            convert_image(filename)
        except Exception as e:
            print "'%s' could not be processed as an image: %s" %(filename, e) 
            try:
                convert_audio(filename)
            except Exception as a:
                print "'%s' could not be processed as audio: %s" %(filename, a) 
                


def convert_image(filename):
    try:
        file1  = Image.open(filename)
        file2  = Image.open(filename)
        filename_1 = next(alt_name
                          for alt_name in alternative_names(OUTPUT_IMG_FOLDER_RESIZED + os.path.splitext(filename)[0] + RESIZED_IMG_FILENAME_SUFFIX + ".jpg")
                          if not os.path.exists(alt_name))
        filename_2 = next(alt_name
                          for alt_name in alternative_names(OUTPUT_IMG_FOLDER_THUMBNAIL + os.path.splitext(filename)[0] + THUMBNAIL_IMG_FILENAME_SUFFIX + ".jpg")
                          if not os.path.exists(alt_name))
        
        print "Converting File: %s with size:(%d x %d)"%(filename, file1.size[0], file1.size[1])
        print "Exporting Resized: %s" % filename_1
        print "Exporting Thumbnail: %s" % filename_2

        w = file1.size[0]
        h = file1.size[1]

        # If width is larger than 368px and height is larger than 275px
        if (w > 368 and h > 275):
            # If width is larger than height            
            if w > h:
                # file1 = Resize height to 275px and crop width to 368px
                file1.thumbnail((w, 275), Image.ANTIALIAS) 
                file1.crop((0,0,368,275))
                
                # file2 = Resize height to 172px and crop width to 208px
                file2.thumbnail((w, 172), Image.ANTIALIAS)
                file2.crop((0,0,208,172))
                
            else:
                # file1 = Resize width to 368px and crop height to 275px
                file1.thumbnail((368, h), Image.ANTIALIAS)
                file1.crop((0,0,368,275))
            
                # file2 = Resize height to 208px and crop width to 172px
                file2.thumbnail((w, 208), Image.ANTIALIAS)
                file2.crop((0,0,172,208))
            
                file2.save(filename_2, "JPEG")
                file1.save(filename_1, "JPEG")
    except Exception as e:
        raise e


def convert_audio(filename):
    
    valid_formats = [".wav", ".aif", ".aiff", ".au", ".mp3",".ogg",".flac",".m4a",".wma",".3gp",".aac"]
    ext = os.path.splitext(filename)[1].lower()

    mp3_filename = next(alt_name
                        for alt_name in alternative_names(MP3_FOLDER + os.path.splitext(filename)[0] + ".mp3")
                        if not os.path.exists(alt_name))
    ogg_filename = next(alt_name
                        for alt_name in alternative_names(OGG_FOLDER + os.path.splitext(filename)[0] + ".ogg")
                        if not os.path.exists(alt_name))

    if any(ext in s for s in valid_formats):
        print "CONVERTING TO MP3:"
        cmdline = [
            'avconv',
            '-y',
            '-i',
            filename,
            mp3_filename,
        ]
        subprocess.call(cmdline)
        print "CONVERTING TO OGG:"
        cmdline = [
            'avconv',
            '-y',
            '-i',
            filename,
            ogg_filename,
        ]
        subprocess.call(cmdline)
    else:
        print "unsupported file extension"
        raise

if __name__ == "__main__":
   main(sys.argv[1:])




