# shorts-vid-stacker

Shorts-vid-stacker is a Python-based tool that utilizes openai's transcription, voice generation, and chat completion apis, along with the ffmpeg CLI to create distinct short-form Youtube videos on various content.

The result is fully automatic AI-generated narrated short form content in a form that entices the user to stay and watch:

![plot](assets/ex-generated.png)

- The top video is an active video that engages the user
- The bottom video is a passive video in case the user gets bored.
- The narration and text transcription is to further engage the user. 

It also has a utility to automatically upload the video to youtube with selenium and chromedriver.

## Installation

1. Clone this repo.

2. Install the required dependencies using pip (NOTE: use conda env and python 3.11).
```bash
conda env create -f environment.yaml
```
3. Setup a `.envrc` file as below (you can use direnv to load these env vars):
    - OPENAI_KEY="user-value"
    - GCS_DEVELOPER_KEY=user-value
    - GCS_CX=user-value

## Usage

1. Add keywords in main.py
2. Add input action and passive videos as well as mp3 files in videos/ and audio/ respectively.
2. Run main.py

## License

[MIT License](LICENSE)


