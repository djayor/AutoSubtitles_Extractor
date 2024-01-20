# AutoSubtitles_Extractor
Shell Script to extract subtitles from *.mkv files to add to a crontab (to execute everyday)

Requirements:
- Linux system with the packages installed:
    - mkvtoolnix
    - mplayer

How to run:
$ ./extract_subtitles.sh /path_of_your_movie_library/

Or can be added to a cron job:
$ crontab -e
Add the line, to run every day at 04:00am:
04 00 * * * /path/to/script/extract_subtitles.sh > ~/extract_subtitles.log

