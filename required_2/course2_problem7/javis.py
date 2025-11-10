import pyaudio
import wave
import os
from datetime import datetime

# 녹음 관련 설정
FORMAT = pyaudio.paInt16  # 오디오 포맷
CHANNELS = 1              # 모노 채널
RATE = 44100              # 샘플링 레이트
CHUNK = 1024              # 버퍼 크기
RECORD_SECONDS = 5        # 녹음 시간 (초)

# 저장 폴더 설정
RECORD_FOLDER = os.path.join(os.path.dirname(__file__), "records")

def ensure_record_folder_exists():
    if not os.path.exists(RECORD_FOLDER):
        os.makedirs(RECORD_FOLDER)

def get_filename():
    now = datetime.now()
    filename = now.strftime("%Y%m%d-%H%M%S") + ".wav"
    return os.path.join(RECORD_FOLDER, filename)

def record_audio():
    ensure_record_folder_exists()
    filename = get_filename()

    audio = pyaudio.PyAudio()

    print("🎤 녹음을 시작합니다...")

    # 마이크 스트림 열기
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("녹음이 완료되었습니다.")

    # 스트림 정리
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 녹음 파일 저장
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"파일 저장 완료: {filename}")

if __name__ == "__main__":
    record_audio()
