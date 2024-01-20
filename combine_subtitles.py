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
        srt1_path = os.path.join(subtitles_path, f"{base_name}.pt.srt")
        srt2_path = os.path.join(subtitles_path, f"{base_name}.pl.srt")

        combined_file_path = os.path.join(subtitles_path, f"{base_name}.srtout")

        if os.path.exists(combined_file_path):
            print(f"Combined .srt file already exists at {combined_file_path}. No need to combine again.")
            continue

        # Check if both .srt files exist before proceeding
        if not os.path.exists(srt1_path) or not os.path.exists(srt2_path):
            print(f"Error: Subtitle files missing for {base_name}. Skipping combination.")
            continue

        with open(srt1_path, 'r', encoding='utf-8') as f:
            srt1 = f.read()

        with open(srt2_path, 'r', encoding='utf-8') as f:
            srt2 = f.read()

        combined_subs = combine_subtitles(srt1, srt2)
        generate_combined_srt(combined_subs, combined_file_path)

        print(f"Subtitle combination complete. Combined file saved at {combined_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python combine_subtitles.py /path/to/subtitles/")
    else:
        main(sys.argv[1])
