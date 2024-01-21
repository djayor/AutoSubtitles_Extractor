# AutoSubtitles_Extractor
Script to extract subtitles from *.mkv files and combine 2 different languages in the same block of subtitles.

This model was created to extract subtitles in Portuguese, Polish and English from .mkv files, will search in folders and subfolders passed by arguments.
Subsequently only 2 sets of subtitles are grouped into a single block, with the first subtitle in **<span style="color:white">white</span>** and the second subtitle in **<span style="color:yellow">yellow</span>**.

Subtitle aggregation has a defined priority according to the existing subtitles. Which will be:
- Portuguese :portugal: / Polish :poland:
- Portuguese :portugal: / English :uk:
- English :uk: / Polish :poland:

If none of these sets can be satisfied, subtitle aggregation is not performed, however it can be added manually and when the script runs again it will be performed.

The subtitles will be extracted and, depending on the language, they will have a different extension:
- Portuguese -> *.pt.srt
- Polish -> *.pl.srt
- English -> *.en.srt

Once combined, they will have the .srt extension, always maintaining the same name as the .mkv file from which they were originally extracted. This way it will facilitate the selection of subtitles in multimedia players such as PLEX, Jellyfin, etc. And they will be appear in the subtitles list as "Unkown subtitle".

Requirements to run the script:
- Linux distro with the packages installed:
    - python3
    - mkvtoolnix
    - mplayer

How to run:
`$ ./extract_subtitles.sh /path/to/your/movie/library/`

Or can be added to a cron job to run everyday:
`$ crontab -e`

Add the line, to run every day at 04:00am (example):

`04 00 * * * /path/to/script/extract_subtitles.sh /path/to/your/movie/library/ > ~/extract_subtitles.log`

