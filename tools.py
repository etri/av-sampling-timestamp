"""
functions
"""

import os
from shutil import copy2

def parse_csv(filepath):
    """
    csv 파일을 입력받아 기재된 timestamps를 리스트 형태로 저장.
    :param filepath: csv file path
    :return timestamps_list: timestamps가 저장된 리스트
    """
    timestamps_list = []
    with open(filepath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.split('\n')[0]
            start = round(float(line.split(',')[0]), 1)
            end = round(float(line.split(',')[1]), 1)

            timestamps_list.append((start, end))

    return timestamps_list

def store_frames(frames_path, store_path, timestamp):
    """
    timestamp 정보를 입력받아 해당 비디오 프레임 이미지 파일을 복사.
    :param frames_path: 비디오 전체 프레임 경로
    :param store_path: 프레임 이미지를 저장할 경로
    :param timestamp: timestamp 정보가 저장된 리스트
    """
    start_frame_idx = int(timestamp[0] * 25)
    end_frame_idx = int(timestamp[1] * 25)

    for idx in range(start_frame_idx, end_frame_idx):
        source = os.path.join(frames_path, '%06d.jpg'%idx)
        target = os.path.join(store_path, '%06d.jpg'%idx)
        copy2(source, target)