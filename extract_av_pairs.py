"""
main function
"""

import os
import subprocess
import sys
import time
import argparse
import warnings
from shutil import rmtree

from tools import parse_csv, store_frames

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description="Extract audiovisual frames")
parser.add_argument('-i', '--input',      type=str,   dest='videoPath',  help='video file path')
parser.add_argument('-c', '--crop',      type=str,   dest='csvPath',  help='crop info file path')
args = parser.parse_args()

# create path
args.store_dirname = args.videoPath.split('.' + args.videoPath.split('.')[-1])[0]
args.video_frames_path = os.path.join(args.store_dirname, 'v_frames')
args.crop_path = os.path.join(args.store_dirname, 'crops')
if os.path.exists(args.store_dirname):
    rmtree(args.store_dirname)
os.makedirs(args.store_dirname)
os.makedirs(args.video_frames_path)
os.makedirs(args.crop_path)

# extract video
args.video_file_path = os.path.join(args.store_dirname, args.videoPath)
command = ("ffmpeg -y -i %s -qscale:v 2 -threads 10 -async 1 -r 25 %s -loglevel panic"
           % (args.videoPath, args.video_file_path))
subprocess.call(command, shell=True, stdout=None)
sys.stderr.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Extract the video and save in %s \r\n"
                 % (args.video_file_path))

# extract the video frames
command = ("ffmpeg -y -i %s -qscale:v 2 -threads 10 -f image2 %s -loglevel panic"
           % (args.video_file_path, os.path.join(args.video_frames_path, '%06d.jpg')))
subprocess.call(command, shell=True, stdout=None)
sys.stderr.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Extract the frames and save in %s \r\n"
                 % (args.video_frames_path))

# extract audio
args.audio_path = os.path.join(args.store_dirname, 'audio.wav')
command = ("ffmpeg -y -i %s -qscale:a 0 -ac 1 -vn -threads 10 -ar 16000 %s -loglevel panic"
           % (args.video_file_path, args.audio_path))
subprocess.call(command, shell=True, stdout=None)
sys.stderr.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Extract the audio and save in %s \r\n"
                 % (args.audio_path))

# crop video and audio
timestamps_list = parse_csv(args.csvPath) # 0.1초 단위 강제 변환
for timestamp in timestamps_list:
    timestamp_dirname = os.path.join(args.crop_path, str(timestamp[0]) + "-" + str(timestamp[1]))
    os.makedirs(timestamp_dirname)
    store_frames(args.video_frames_path, timestamp_dirname, timestamp)

    audio_path = os.path.join(timestamp_dirname, 'audio.wav')
    command = (
            "ffmpeg -y -i %s -async 1 -ac 1 -vn -acodec pcm_s16le -ar 16000 -threads 10 -ss %.3f -to %.3f %s"
            % (args.audio_path, timestamp[0], timestamp[1], audio_path))
    subprocess.call(command, shell=True, stdout=None)  # Crop audio file

print("Done")