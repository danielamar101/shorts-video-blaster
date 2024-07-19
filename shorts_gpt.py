#!/usr/bin/env python
from openai import OpenAI
import os
import requests
import io
import subprocess
from pydub import AudioSegment
import json
import random


client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

video_path = './videos/swimmer.mp4'
audio_path = './audio/output_audio.mp3'
output_path = './done/output.mp4'

def get_media_duration(file_path):
    # Command to get the duration of the media file in seconds
    cmd_get_duration = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
    duration = subprocess.check_output(cmd_get_duration).decode('utf-8').strip()
    return float(duration)


def text_to_speech(input, audio_path, speed=1.0, voice=random):

    if voice == 'random':

        voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        voice = random.choice(voices)
    
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        json={
            "model": "tts-1-1106",
            "input": input,
            "voice": voice,
            "speed": speed
        },
    )

    audio = b""
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        audio += chunk

  # Assuming the API returns audio in a format like WAV or OGG
    audio_data = audio

    # Create an AudioSegment instance from the audio data
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")  # Adjust format if necessary

    # Export the audio segment to an MP3 file
    audio_segment.export(audio_path, format="mp3")

def highlight_random_word(srt_text):
    # Define the color for highlighting
    highlight_color = "#FF0000"
    
    # Split the SRT text into lines
    lines = srt_text.split('\n')
    
    # Process each line
    for i, line in enumerate(lines):
        if not line.isdigit() and '-->' not in line and line.strip():
            words = line.split()
            if words:
                # Select a random word to highlight
                random_word = random.choice(words)
                highlighted = f'<font color="{highlight_color}">{random_word}</font>'
                
                # Replace the word in the line
                lines[i] = line.replace(random_word, highlighted, 1)


    
    # Join the lines back into a single string
    return '\n'.join(lines)

def convert_to_srt(data):
    srt_content = ""
    subtitle_index = 1
    words_in_subtitle = []
    start_time = 0
    end_time = 0

    # Randomly decide how many words to group (2-4)
    words_to_group = random.randint(1, 2)

    for i, word_info in enumerate(data['words']):
        if not words_in_subtitle:  # Start of a new group
            start_time = word_info['start']
        
        words_in_subtitle.append(word_info['word'].upper())
        end_time = word_info['end']  # Always update to the last word's end time

        # Group words when the limit is reached or it's the last word
        if len(words_in_subtitle) >= words_to_group or i == len(data['words']) - 1:
            start_srt = f"{int(start_time // 3600):02}:{int(start_time % 3600 // 60):02}:{int(start_time % 60)},{int(start_time % 1 * 1000):03}"
            end_srt = f"{int(end_time // 3600):02}:{int(end_time % 3600 // 60):02}:{int(end_time % 60)},{int(end_time % 1 * 1000):03}"
            
            sentence = ' '.join(words_in_subtitle)
            srt_content += f"{subtitle_index}\n{start_srt} --> {end_srt}\n{sentence}\n\n"
            
            # Reset variables for the next group
            words_in_subtitle = []
            subtitle_index += 1
            words_to_group = random.randint(1, 2)  # Decide again for the next group

    return highlight_random_word(srt_content)

def audio_to_srt(audio_path, transcript_path, granularity="word"):
    global client
    audio_file = open(audio_path, "rb")
    append_params = {}

    if granularity == 'word':
        append_params['response_format'] = 'verbose_json'
    else:
        append_params['response_format'] = 'srt'


    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        timestamp_granularities=[granularity],
        **append_params
    )

    if type(transcript) is str:
        with open(transcript_path, 'w') as file:
                file.write(transcript)
    else:
        with open(transcript_path, 'w') as file:
            file.write(convert_to_srt(transcript.model_dump()))
            # file.write(json.dumps(transcript.model_dump()))


def gpt_generate(system,text, mode="text"):
    global client
    completion = client.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages = [{"role": "system", "content" : system},
                {"role": "user", "content" : text}],
                response_format={ "type": mode }
                )
def gpt_generate(system,text, mode="text"):
    global client
    completion = client.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages = [{"role": "system", "content" : system},
                {"role": "user", "content" : text}],
                response_format={ "type": mode }
                )
    
    return(completion.choices[0].message.content)

    
def gpt_generate_no_sys(text, mode="text"):
    global client
    completion = client.chat.completions.create(
                model="gpt-4-1106-preview", 
                messages = [{"role": "user", "content" : text}],
                response_format={ "type": mode }
                )
    
    return(completion.choices[0].message.content)


def generate_fun_facts_prompt(amt_facts):
    sys_prompt = """

    """
    # fun_fact_prompt = """
    # Given a keyword, you return {} fun facts related to that keyword. The keyword should exist within each fun fact at any point if possible. 
    # Strictly follow the syntax:
    # {{
    #     facts: [fun fact 1, fun fact 2, fun fact 3, fun fact 4]
    # }}

    # Each topic should be distinct and cover a wide breath of the keyword. 
    # You must return a valid json list that follows the given syntax.
    # """.format(amt_facts)

    fun_fact_prompt = """
        Given a keyword, you return {} fun facts related to that keyword and create a short voiceover script in a style that is engaging for short-term media sites like Youtube Shorts or TikTok. 
        Make sure the start of the script has an introductory sentence that intices the user to stay and watch for longer. Try to make each sentence an artistic cliff hanger leaving the user on the edge of their seat.
        Make each fun fact short and succinct so that the total length of the script when read out loud does not exceed one minute.
        The keyword should exist within each fun fact at any point if possible. 
        Each fact should be distinct and cover a diverse portion of the keyword. Do not use any emojis. Each fun fact should be brief. Be sure to tell the user to like and subscribe at the end of the script.
    """.format(amt_facts)

    return fun_fact_prompt

def get_fun_facts_from_keyword(keyword, num_facts):
    user_msg = generate_fun_facts_prompt(num_facts)
    text=gpt_generate(user_msg,keyword,'text')
        
    print("Response:")
    print(text)

    return text


def generate_jokes_prompt(amt_facts):

    joke_prompt = """
        Given a keyword, you return {} jokes related to that keyword and create a short voiceover script in a style that is engaging for short-term media sites like Youtube Shorts or TikTok. 
        Make sure the start of the script has an introductory sentence that intices the user to stay and watch for lthe entire duration of the video.
        Make each joke succinct so that the total length of the script when read out loud does not exceed one minute.
        The keyword should exist within each joke at any point if possible. 
        Each fact should be distinct and cover a diverse portion of the keyword. Do not use any emojis. IMPORTANT: Make sure to tell the user to like and subscribe at the end of the script.
    """.format(amt_facts)

    return joke_prompt


def generate_marcus_quotes_prompt(amt_facts):

    marcus_prompt = """
        Give me a Marcus Aurelias quote about the meaning of life that invoke emotion.
        Jump right into the quote and deliver a great life lesson to the user to help them go about their day.
        Make sure the quote is deep and explain it like joe rogan does his podcasts, but keep the fact that you're explaining it like joe rogan secret in the script. 
        
        Do not use any emojis. 
        IMPORTANT: Make sure to tell the user to like and subscribe at the end of the script.
    """.format(amt_facts)

    return marcus_prompt


def generate_philos_quotes_prompt():

    philosophy_prompt = """
        Your job is to make a quote for a Youtube Shorts video. You are the narrator of the video so make the languge you create flow like you are giving a presentation.
        
        After reading the one deep and powerful quote, be sure to explain who said it.
    
        Briefly explain it the meaning behind the philosophy in a way a 5 year old can understand.
        Jump right into the lesson and deliver a great life lesson to the user to help them go about their day.
        
        Do not use any emojis. 
        IMPORTANT: Make sure to tell the user to like and subscribe at the end of the script.
    """

    return philosophy_prompt

def generate_philos_quotes_prompt_structured():

    philosophy_prompt = """
        Your job is to make a quote for a Youtube Shorts video. You are the narrator of the video so make the languge you create flow like you are giving a presentation.
        
        After reading the one deep and powerful quote, be sure to explain who said it. 
    
        Briefly explain it the meaning behind the philosophy in a way a 5 year old can understand.
        Jump right into the lesson and deliver a great life lesson to the user to help them go about their day.
        
        Do not use any emojis. 
        IMPORTANT: Make sure to tell the user to like and subscribe at the end of the script.

        Return the script narration, as well as a catchy title and short description of the video in the json format denoted below:
        ```
        {
            script: <script here>,
            title: <title here>,
            description: <description here>,
        }
        ```
    """

    return philosophy_prompt

def get_quotes_for_marcus(keyword, num_facts):
    user_msg = generate_marcus_quotes_prompt(1)
    text=gpt_generate(user_msg,'Give me the marcus aurelias script in the form I requested.','text')
        
    print("Response:")
    print(text)

    return text

def get_deep_quote_script():
    user_msg = generate_philos_quotes_prompt()
    text=gpt_generate_no_sys(user_msg,'text')
        
    print("Response:")
    print(text)

    return text

def get_deep_quote_script_structured():
    user_msg = generate_philos_quotes_prompt_structured()
    text=gpt_generate_no_sys(user_msg,'json_object')

    return text

def get_jokes_from_keyword(keyword, num_facts):
    user_msg = generate_jokes_prompt(num_facts)
    text=gpt_generate(user_msg,keyword,'text')
        
    print("Response:")
    print(text)

    return text





if __name__ == "__main__":
    get_fun_facts_from_keyword('Minecraft', 3)



