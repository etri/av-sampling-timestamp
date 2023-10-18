## AV Sampling Timestamp

비디오 파일과 timestamp 정보가 저장된 csv 파일을 입력받아,
전체 비디오 프레임 및 오디오 파일 추출 그리고 timestamp 별 비디오 프레임 및 오디오 파일 추출을 위한 소스코드입니다.

timestamp 정보가 저장된 csv 파일은 아래 예시와 같이 0.1초 단위로 작성되어야 함. (시작점, 끝점)
```
1.2,2.2
6.0,10.0
```

### Dependencies

Start from building the environment
```
conda create -n asd-dp python=3.7
conda activate asd-dp
pip install -r requirement.txt
```

Start from the existing environment
```
pip install -r requirement.txt
```

### Usage

1. 비디오 파일 및 timestamp 정보가 저장된 csv 파일의 경로를 포함하여 아래 명령어와 같이 실행.
```
python extract_av_pairs.py -i VideoPath -c CsvPath

for example,
python extract_av_pairs.py -i test.avi -c crops.csv
```

2. 비디오 파일명과 동일한 디렉토리가 새로 생성되며, crops 폴더에서 추출 결과물 확인 가능.
```
input_video 폴더
 - crops : timestamp 별 비디오 프레임 및 오디오 파일 저장 폴더
 - v_frames : 전체 비디오 프레임 저장 폴더
 - audio.wav : 전체 오디오 파일
 - video.mp4 : 비디오 파일 재인코딩 (25fps 등)
```

### Authors
복합지능연구실 경민영 mykyoung@etri.re.kr