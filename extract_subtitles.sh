#!/bin/bash

# Check if a path is provided
if [ -z "$1" ]; then
  echo "Please provide the path to the directory containing MKV files."
  exit 1
fi

# Change to the specified directory
cd "$1" || exit

# Find all MKV files in the directory and its subdirectories
find . -type f -name "*.mkv" -print0 | while read -r -d $'\0' file; do
  # Extract the base name without extension
  base_name=$(basename -s .mkv "$file")

  # Use mplayer to identify subtitle tracks and extract the lines with language codes
  mplayer_output=$(mplayer -vo null -ao null -frames 0 "$file" 2>&1)

  # Find lines containing language codes and save them
  por_line=$(echo "$mplayer_output" | grep -iP '(?=.*\bpor\b)(?=.*\bsrt\b)' | grep -oP 'stream \K[0-9]+')
  pol_line=$(echo "$mplayer_output" | grep -iP '(?=.*\bpol\b)(?=.*\bsrt\b)' | grep -oP 'stream \K[0-9]+')
  eng_line=$(echo "$mplayer_output" | grep -iP '(?=.*\beng\b)(?=.*\bsrt\b)' | grep -oP 'stream \K[0-9]+')

  # Extract track numbers from saved lines
  por_track=$(echo "$por_line" | head -n 1)
  pol_track=$(echo "$pol_line" | head -n 1)
  eng_track=$(echo "$eng_line" | head -n 1)

  # Function to check if a subtitle file exists
  subtitle_exists() {
    local track="$1"
    [ -f "$(dirname "$file")/${base_name}.${track}.srt" ]
  }

  # Check and extract Portuguese subtitle track
  if [ -n "$por_track" ]; then
    if subtitle_exists "pt"; then
      echo "Portuguese subtitle already exists for $file"
    else
      mkvextract tracks "$file" "$por_track":"$(dirname "$file")/${base_name}.pt.srt"
      echo "Portuguese subtitle extracted for $file"
    fi
  else
    echo "No Portuguese subtitle track found for $file"
  fi

  # Check and extract Polish subtitle track
  if [ -n "$pol_track" ]; then
    if subtitle_exists "pl"; then
      echo "Polish subtitle already exists for $file"
    else
      mkvextract tracks "$file" "$pol_track":"$(dirname "$file")/${base_name}.pl.srt"
      echo "Polish subtitle extracted for $file"
    fi
  else
    echo "No Polish subtitle track found for $file"
  fi

  # Check and extract English subtitle track
  if [ -n "$eng_track" ]; then
    if subtitle_exists "en"; then
      echo "English subtitle already exists for $file"
    else
      mkvextract tracks "$file" "$eng_track":"$(dirname "$file")/${base_name}.en.srt"
      echo "English subtitle extracted for $file"
    fi
  else
    echo "No English subtitle track found for $file"
  fi
done

sleep 10
echo "Subtitle extraction complete."

python3 ~/combine_subtitles.py $1

directory=$1

# Find and rename .srtout.srt files to .srt recursively
find "$directory" -type f -name '*.srtout.srt' -exec bash -c 'mv "$1" "${1%.srtout.srt}.srt"' _ {} \;

sleep 10
echo "Subtitle combination complete."