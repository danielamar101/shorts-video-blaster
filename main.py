from shorts_gpt import get_fun_facts_from_keyword, text_to_speech, get_jokes_from_keyword, get_quotes_for_marcus, audio_to_srt, get_deep_quote_script, get_deep_quote_script_structured
from shorts_vid_stacker import shorten_and_stack_two_videos
from utilities.get_random_video_paths import get_random_video_path, get_random_audio_path
from utilities.bot_yt_upload import upload_youtube_video
import json


keyword = 'nlp-meeting-demo-video'

print(f"Creating video...")
# fun_facts = get_fun_facts_from_keyword(keyword, 2)
# jokes = get_jokes_from_keyword(keyword, 6)
# jokes = get_quotes_for_marcus(keyword, 1)
# quote_script = get_deep_quote_script()
quote_script = get_deep_quote_script_structured()
quote_script = json.loads(quote_script)
print(quote_script)
print('...done')

transcribed_audio = './generations/audio.mp3'

print(f"Creating text to speech for fun facts about {keyword}...")
# text_to_speech(fun_facts,output_audio, speed=1.35)
text_to_speech(quote_script['script'],transcribed_audio, speed=1, voice='random')
print('...done')

# Get audio transcription srt format
transcript_path = './generations/transcript.srt'
print("transcribing audio...")
audio_to_srt(transcribed_audio,transcript_path)
print("...done")

overlay_audio = get_random_audio_path()

video_path_1 = get_random_video_path(action=True)
video_path_2 = get_random_video_path(action=False)

generated_final_path = f'./generations/{keyword}-final-gen.mp4'

print(f'Generating a double stacked video file from {video_path_1} and {video_path_2}.')
print(f'Will then take the audio from the text to speech and combine them all together.')
print(f'I will output this final video to {generated_final_path}')

shorten_and_stack_two_videos(video_path_1=video_path_1, video_path_2=video_path_2,audio_path=overlay_audio, tts_path=transcribed_audio, transcript_path=transcript_path, output_path=generated_final_path)

print(f'...done. Output video in {generated_final_path}')

# upload_youtube_video(generated_final_path,quote_script['title'], quote_script['description'])