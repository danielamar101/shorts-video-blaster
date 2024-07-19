import os
import random

def get_random_video_path(action=False):
    # Replace the placeholder path with your actual video directory path
    video_directory_path = '../videos'

    if action:
        video_directory_path += '/action'
    else:
        video_directory_path += '/passive'

    # Attempt to list all files in the specified directory and filter out only video files if needed
    try:
        video_files = [f for f in os.listdir(video_directory_path) if os.path.isfile(os.path.join(video_directory_path, f))]
        # add a condition to filter for specific video file extensions (e.g., .mp4, .mov)
        video_files = [f for f in video_files if f.endswith('.mp4') ]
        
        # Choose a random video from the list
        random_video = random.choice(video_files) if video_files else None
        print(f"Randomly selected video: {random_video}")
        return f"{video_directory_path}/{random_video}"
    except FileNotFoundError:
        print(f"Directory not found: {video_directory_path}")


def get_random_audio_path():

    audio_directory_path = '../audio'

    try:
        audio_files = [f for f in os.listdir(audio_directory_path) if os.path.isfile(os.path.join(audio_directory_path, f))]
        # add a condition to filter for specific video file extensions (e.g., .mp4, .mov)
        audio_files = [f for f in audio_files if f.endswith('.mp3')]
        
        # Choose a random video from the list
        random_video = random.choice(audio_files) if audio_files else None
        print(f"Randomly selected video: {random_video}")
        return f"{audio_directory_path}/{random_video}"
    except FileNotFoundError:
        print(f"Directory not found: {audio_directory_path}")