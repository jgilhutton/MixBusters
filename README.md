# MixBusters
This script:
- Downloads the audio from YouTube.
- Looks into the video description for some tracklist and RegExes the $H!T out of it, searching for timestamps and song names.
- Uses the tracklist timestamps to slice the audio file and
- Generates a file for each song.... 
- Hopefully.

Slicing is based on minimum dB in order to get the best out of crossfaded audio tracks <-- those are a pain in the a$$.

Usage:
``python MixBusters.py https://www.youtube.com/watch?v=OPb05NFrobo``

# Supported tracklist formats:

> 04 06:16 Artist - Song



> Artist - Song 06:16



> *06:16 Artist - Song

> 01:33:12 Artist - Song



  

# Requirements:
- [ffmpeg](https://www.ffmpeg.org/download.html). Binaries must be in $PATH, otherwise you must specify ffmpeg fullpath on the script's command strings.
- pytube python module. I'm really hoping to get rid of the module. It does a whole bunch of stuff we don't need for this to work. Getting this script to work without pytube would be neat.
Meanwhile: ``pip install pytube``
