# 모든 영상 함수 하나로 재생하기

!pip install ffmpeg-python

# ffmpeg : 다양한 멀티미디어 작업을 수행할 수 있는 오픈 소스
# ffmpeg-python : 파이썬에서 사용할 수 있게 만든 파이썬 래퍼(wrapper)
import ffmpeg
from base64 import b64encode
from IPython.display import HTML

def get_video_metadata(video_path):
    try:
        # 입력 파일의 정보를 가져옴
        probe = ffmpeg.probe(video_path)
        # print(probe)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        return {
            'video_codec': video_stream['codec_name'] if video_stream else 'None',
        }
    except Exception as e:
        return {'error': str(e)}

def convert_video_to_h264(input_path, output_path):
    try:
        ffmpeg.input(input_path).output(output_path, vcodec='libx264').run(overwrite_output=True)
        return True
    except ffmpeg.Error as e:
        return False

# 영상 파일의 메타데이터를 확인하고 h264 방식으로 압축
def check_and_convert_video(video_path):
    metadata = get_video_metadata(video_path)

    if metadata.get('error'):
        return f"Error retrieving metadata: {metadata['error']}", 0

    if metadata['video_codec'] == 'mpeg4':
        output_path = video_path.replace('.mp4', '_converted.mp4')
        success = convert_video_to_h264(video_path, output_path)
        if success:
            return output_path, 1
        else:
            return "Failed to convert video.",0
    else:
        return video_path, 2

# 영상 파일을 인코딩하고 웹페이지에 출력
def play_video(video_path):
    play_video_file, result = check_and_convert_video(video_path)

    if result!=0:
        # 비디오 파일을 읽고 base64로 인코딩
        try:
            with open(play_video_file, "rb") as video_file:
              # base64 : Binary Data를 Text로 바꾸는 Encoding
              video_encoded = b64encode(video_file.read()).decode('ascii')

            # HTML 코드 생성
            video_html = f'''
            <video width=800 controls>
            <source src="data:video/mp4;base64,{video_encoded}" type="video/mp4">
            </video>
            '''
            display(HTML(video_html))
        except Exception as e:
            print(f"Error: {e}")
    else :
        print("unknown file!!!")
