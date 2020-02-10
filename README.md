# HAARP - HTTP Anti Audiophile Reencoding Proxy

This little program starts a webserver which hosts audio files from a defined directory. The audio files are detected by the filename suffix. The audio files are converted to mp3 while downloading. it also tries to read mpdignore files and fails miserably, but my requirements are low enough

## Why
i have a lot of flac files which would take up lots of space on my phone, so i thought of a way to already convert them while downloading them to it

## how to run

idk its a small, mostly one-time utility, i wouldn't bother setting up uwsgi. if you want to, search on google for hosting flask projects. i just use the included `devserv.sh` file which starts up flash in development mode which seems to work fine enough

## ok now how to download files created with this magic piece of software

i use `wget -r` with termux


TODO: make it actually follow .mpdignore properly