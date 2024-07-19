import subprocess
import requests
from bs4 import BeautifulSoup


def get_youtube_video(link, out_dir):
    # yt-dlp https://www.youtube.com/watch?v=a5B8Xx1RPSc --remux-video mp4
    download_and_save_vid = [
    'yt-dlp', link, '-o', f'{out_dir}/%(title)s.%(ext)s', '--remux-video', 'mp4'
    ]
    print("DOWNLOADING VIDEO FROM URL:")
    subprocess.run(download_and_save_vid, check=True)
    


link = 'https://www.youtube.com/watch?v=LfPOD7gbpzk'
video_type="action"
get_youtube_video(link=link,out_dir=f'../../videos/{video_type}')


# def fetch_urls(url):
#     # Fetch the HTML content of the given URL
#     response = requests.get(url)
#     # Use BeautifulSoup to parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Find all anchor tags and extract href attributes
#     urls = [a.get('href') for a in soup.find_all('a') if a.get('href') is not None]
    
#     return urls

# # Example usage
# url = 'https://www.youtube.com/@FreeHDvideosnocopyright/videos'
# print(fetch_urls(url))