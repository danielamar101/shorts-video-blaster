#!/usr/bin/env python
import random
from openai import OpenAI
import os
import subprocess
import json
from shorts_gpt import audio_to_srt

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

video_path = './videos/swimmer.mp4'
audio_path = './audio/output_audio.mp3'
output_path = './done/output.mp4'

def get_media_info(video_path):
    """Retrieve video width, height, and duration using ffprobe."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,duration',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return json.loads(result.stdout)

def delete_clipped_video(clipped_video_path):
    # Check if file exists
    if os.path.exists(clipped_video_path):
        # Delete the file
        os.remove(clipped_video_path)
        print(f"The file {clipped_video_path} has been deleted successfully.")
    else:
        print(f"The file {clipped_video_path} does not exist.")

def generate_clips(video_path='', audio_path='', start_point=0, num=0, target_width=None, target_height=None):
    # Generate ffmpeg command to clip and optionally crop the video.\
    
    input_path = audio_path if audio_path != '' else video_path
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    if input_path == audio_path:
        clipped_path = f'{base_name}_gen_audio.mp3'
    else:
        clipped_path = f'{base_name}_clipped_{num}.mp4'


    out_path = f'../clipped/{clipped_path}'
    cmd_clip = ['ffmpeg', '-i', input_path, '-ss', str(start_point), '-t', '60', '-y']  # Duration of the clip

    if target_width and target_height:
        filter_str = f"crop={target_width}:{target_height}"
        cmd_clip += ['-vf', filter_str]

    # append output path path
    cmd_clip.append(out_path)

    print(f"CLIP GENERATING FROM FILE: {input_path}")
    subprocess.run(cmd_clip, check=True)
    print(f"CLIP GENERATED FROM FILE: {input_path}")

   

    return out_path

def adjust_video_size(video_info_1, video_info_2):
    """Determine target width and height based on smaller dimensions."""
    width_1, height_1 = video_info_1['streams'][0]['width'], video_info_1['streams'][0]['height']
    width_2, height_2 = video_info_2['streams'][0]['width'], video_info_2['streams'][0]['height']

    target_width = min(width_1, width_2)
    target_height = min(height_1, height_2)

    return target_width, target_height

def shorten_and_stack_two_videos(video_path_1, video_path_2, audio_path,tts_path, transcript_path, output_path):
    video_info_1 = get_media_info(video_path_1)
    video_info_2 = get_media_info(video_path_2)
    audio_info = get_media_info(video_path_2)
    video_duration_1 = int(float(video_info_1['streams'][0]['duration']))
    video_duration_2 = int(float(video_info_2['streams'][0]['duration']))
    audio_duration = int(float(audio_info['streams'][0]['duration']))

    if video_duration_1 < 60 or video_duration_2 < 60:
        raise ValueError("Both videos must be at least 60 seconds long")
    
    # Generate 1 minute long clips from input videos, match their dimensions
    start_point_1 = random.randint(1, video_duration_1 - 60)
    start_point_2 = random.randint(1, video_duration_2 - 60)
    start_point_3 = random.randint(1,  audio_duration - 60)
        
    target_width, target_height = adjust_video_size(video_info_1, video_info_2)

    clipped_video_1 = generate_clips(video_path=video_path_1, start_point=start_point_1, num=1, target_width=target_width,target_height=target_height)
    clipped_video_2 = generate_clips(video_path=video_path_2, start_point=start_point_2, num=2, target_width=target_width, target_height=target_height)

    clipped_audio = generate_clips(audio_path=audio_path,start_point=start_point_3, num=1)

    # Updated command to stack the clipped videos instead of the original videos
    cmd_adjust_and_combine = [
        'ffmpeg',
        '-i', clipped_video_1,
        '-i', clipped_video_2,
        '-i', tts_path,
        '-i', clipped_audio,
        '-filter_complex',
        f"""
        [0:v][1:v]vstack=inputs=2[stacked];  
        [stacked]scale=-2:'2*ih*9/16'[adjusted];  
        [adjusted]pad='iw':'max(ih,iw*16/9)':(ow-iw)/2:(oh-ih)/2:black[v_stack];
        [v_stack]subtitles={transcript_path}:force_style='Alignment=10,FontName=Cochin,FontSize=12,Bold=1,PrimaryColour=&H00ffffff,OutlineColour=&H00000000,BackColour=&H00000000,BorderStyle=1,fontfile=fonts/SuperRugged.ttf'[v_with_subs];
        [3:a]volume=0.04[a_adjusted];
        [2:a][a_adjusted]amix=inputs=2:duration=shortest[a_mix]
        """, 
        '-map', '[v_with_subs]', 
        '-map', '[a_mix]', # Map the video from the filter and audio from the audio file
        '-shortest',
        '-y',  # Overwrite output file without asking
        output_path,
    ]

    print("STACKING VIDEOS NOW...")
    subprocess.run(cmd_adjust_and_combine, check=True)

    print("Cleaning up clipped videos")
    delete_clipped_video(clipped_video_1)
    delete_clipped_video(clipped_video_2)



if __name__ == '__main__':
    # base64Frames = import_video()

    # # description = create_description_from_video(base64Frames=base64Frames)
    # script = create_script_from_video(base64Frames=base64Frames)
    
    video_path_1 = './videos/mc.mp4'
    video_path_2 = './videos/mc.mp4'

    #shorten_and_stack_two_videos(video_path_1, video_path_2, output_path)




