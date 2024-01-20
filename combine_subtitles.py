from datetime import datetime, timedelta
import re
from html import escape
import os
import sys

def parse_srt(srt_content):
    subs = []
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)\n\n', re.DOTALL)
    matches = pattern.findall(srt_content)
    for match in matches:
        index, start, end, text = match
        start_time = datetime.strptime(start, "%H:%M:%S,%f")
        end_time = datetime.strptime(end, "%H:%M:%S,%f")
        subs.append((index, start_time, end_time, text))
    return subs

def combine_subtitles(srt1, srt2):
    subs1 = parse_srt(srt1)
    subs2 = parse_srt(srt2)

    combined_subs = []
    threshold = timedelta(milliseconds=1000)

    for sub1 in subs1:
        combined_subs.append(f"{sub1[0]}\n{sub1[1].strftime('%H:%M:%S,%f')[:-3]} --> {sub1[2].strftime('%H:%M:%S,%f')[:-3]}\n")
        combined_subs[-1] += f'<font color="#ffffff">{escape(sub1[3])}</font>\n'

        for sub2 in subs2:
            if sub1[1] - threshold <= sub2[2] and sub1[2] + threshold >= sub2[1]:
                combined_subs[-1] += f'<font color="#fffb00">{escape(sub2[3])}</font>\n'

        combined_subs[-1] += '\n'  # Add a newline to separate subtitle blocks

    return combined_subs

def generate_combined_srt(combined_subs, base_name):
    combined_file_path = f"{base_name}.srt"

    with open(combined_file_path, 'w', encoding='utf-8') as f:
        for line in combined_subs:
            f.write(line)

    return combined_file_path

def main(subtitles_path):
    srt_files = [f for f in os.listdir(subtitles_path) if f.endswith(".srt")]

    if len(srt_files) < 2:
        print("Error: At least two .srt files are required for combining subtitles.")
        return

    base_names = set(os.path.splitext(f.rsplit('.', 1)[0])[0] for f in srt_files)

    for base_name in base_names:
        combined_file_path = os.path.join(subtitles_path, f"{base_name}.srtout")
        combined_file_path_with_extension = os.path.join(subtitles_path, f"{base_name}.srtout.srt")
        combined_file_path_base = os.path.join(subtitles_path, f"{base_name}.srt")

        if os.path.exists(combined_file_path_with_extension):
            print(f"Combined .srt file already exists at {combined_file_path_with_extension} - No need to combine again.")
            continue
        
        if os.path.exists(combined_file_path_base):
            print(f"Combined .srt file already exists at {combined_file_path_base} - No need to combine again.")
            continue

        srt1_path = os.path.join(subtitles_path, f"{base_name}.pt.srt")
        srt2_path = os.path.join(subtitles_path, f"{base_name}.pl.srt")
        srt3_path = os.path.join(subtitles_path, f"{base_name}.en.srt")

        # Check if at least two subtitle files exist before proceeding
        subtitle_paths = [srt1_path, srt2_path, srt3_path]
        subtitle_paths = [path for path in subtitle_paths if os.path.exists(path)]

        if len(subtitle_paths) < 2:
            print(f"Error: Insufficient subtitle files for {base_name}. Skipping combination.")
            continue

        # Define priority order for language pairs
        language_priority = [('pt', 'pl'), ('pt', 'en'), ('en', 'pl')]

        for lang1, lang2 in language_priority:
            lang1_path = os.path.join(subtitles_path, f"{base_name}.{lang1}.srt")
            lang2_path = os.path.join(subtitles_path, f"{base_name}.{lang2}.srt")

            if lang1_path in subtitle_paths and lang2_path in subtitle_paths:
                with open(lang1_path, 'r', encoding='utf-8') as f1:
                    srt1 = f1.read()

                with open(lang2_path, 'r', encoding='utf-8') as f2:
                    srt2 = f2.read()

                combined_subs = combine_subtitles(srt1, srt2)
                generate_combined_srt(combined_subs, combined_file_path)

                print(f"Subtitle combination complete. Combined file saved at {combined_file_path}")
                break
        else:
            print(f"No suitable language pair found for {base_name}. Skipping combination.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python combine_subtitles.py /path/to/subtitles/")
    else:
        main(sys.argv[1])
