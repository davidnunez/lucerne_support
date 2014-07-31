#!/usr/bin/python

"""process_upload_file.py: Converts images."""
# Requires:
# sudo apt-get install libogg-dev libvorbis-dev lame libfaad2 libjpeg-dev zlib1g-dev libtiff4  libfreetype6-dev 
# sudo apt-get install liblcms liblcms-dev liblcms-utils libwebp-dev openjpeg-tools tk
# cd ~;wget https://bootstrap.pypa.io/get-pip.py; sudo python get-pip.py
# pip install pillow  # For Image processing
# sudo apt-get install ubuntu-restricted-extras 

import os,sys,itertools, subprocess
from PIL import Image

__author__ = "David Nunez"
__email__  = "dnunez@media.mit.edu"

OUTPUT_IMG_FOLDER_ORIGINAL = "/var/www-lucerne/LocativeSoundShare/client/upload/img/feed/"
OUTPUT_IMG_FOLDER_RESIZED = "/var/www-lucerne/LocativeSoundShare/client/upload/img/feed/"
OUTPUT_IMG_FOLDER_THUMBNAIL = "/var/www-lucerne/LocativeSoundShare/client/upload/img/feed/"

ORIGINAL_IMG_FILENAME_PREFIX = ""
RESIZED_IMG_FILENAME_PREFIX = "resized_"
THUMBNAIL_IMG_FILENAME_PREFIX = "thumbnail_"

MP3_FOLDER = "/var/www-lucerne/LocativeSoundShare/client/upload/snd/mp3/"
OGG_FOLDER = "/var/www-lucerne/LocativeSoundShare/client/upload/snd/ogg/"

valid_audio_formats = [".wav", ".aif", ".aiff", ".au", ".mp3",".ogg",".flac",".m4a",".wma",".3gp",".aac"]

def alternative_names(filename):
    yield filename
    base, ext = os.path.splitext(filename)
    yield base + "_1" + ext
    for i in itertools.count(1):
        yield base + "_%i" % i + ext

def main(argv):
    for filename in argv:
        try:
            ext = os.path.splitext(filename)[1].lower()
            if any(ext in s for s in valid_audio_formats):
                convert_audio(filename)
            else:
                convert_image(filename)
        except Exception as e:
            print "'%s' could not be processed: %s" %(filename, e)

def convert_image(filename):
    try:
        print "made it here"
        filename_base = os.path.basename(filename)
    
    
        filename_1 = next(alt_name
                          for alt_name in alternative_names(OUTPUT_IMG_FOLDER_RESIZED + RESIZED_IMG_FILENAME_PREFIX + os.path.splitext(filename_base)[0] + ".jpg")
                          if not os.path.exists(alt_name))
        filename_2 = next(alt_name
                          for alt_name in alternative_names(OUTPUT_IMG_FOLDER_THUMBNAIL + THUMBNAIL_IMG_FILENAME_PREFIX + os.path.splitext(filename_base)[0] + ".jpg")
                          if not os.path.exists(alt_name))
                                                        
        #        print "Converting File: %s with size:(%d x %d)"%(filename, file1.size[0], file1.size[1])
        print "Exporting Resized: %s" % filename_1
        
        cmdline = [
            'convert',
            filename,
            '-thumbnail',
            '368x275^',
            '-gravity',
            'center',
            '-extent',
            '368x275',
            filename_1
        ]

        print "Exporting Thumbnail: %s" % filename_2
        subprocess.call(cmdline)
        cmdline = [
            'convert',
            filename,
            '-thumbnail',
            '208x172^',
            '-gravity',
            'center',
            '-extent',
            '208x172',
            filename_2
        ]
        subprocess.call(cmdline)

    except Exception as e:
        raise e


def convert_audio(filename):
    filename_base = os.path.basename(filename)
    
    ext = os.path.splitext(filename)[1].lower()

    mp3_filename = next(alt_name
                        for alt_name in alternative_names(MP3_FOLDER + os.path.splitext(filename_base)[0] + ".mp3")
                        if not os.path.exists(alt_name))
    ogg_filename = next(alt_name
                        for alt_name in alternative_names(OGG_FOLDER + os.path.splitext(filename_base)[0] + ".ogg")
                        if not os.path.exists(alt_name))

    if any(ext in s for s in valid_audio_formats):
        print "CONVERTING TO MP3: %s becomes %s"%(filename, mp3_filename)
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




