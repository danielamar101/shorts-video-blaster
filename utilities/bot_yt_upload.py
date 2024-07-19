import time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

# NOTE: USE vid-blaster conda env!
# python -c 'import platform; print(platform.platform())'
# conda env config vars set CONDA_SUBDIR=osx-arm64
def upload_youtube_video(filepath, title='', description=''):
    chrome_options = Options()

    #Find the data path and profile for mac os
    chrome_options.add_argument(r"--user-data-dir=/Users/danielamar/Library/Application Support/Google/Chrome/") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    chrome_options.add_argument(r'--profile-directory=Profile 8')
    
    # Specify the path to chromedriver
    service = Service(executable_path="/Users/danielamar/Desktop/Code/video-blaster/VideoBlaster/shorts-vid-stacker/utilities/chromedriver")
    
    # Initialize the driver with the specified service
    bot = webdriver.Chrome(service=service, options=chrome_options)

    with open('/Users/danielamar/Desktop/Code/video-blaster/VideoBlaster/shorts-vid-stacker/utilities/cookies.json', 'r') as cookies_file:
        cookies = json.load(cookies_file)
        for cookie in cookies:
            # In case of problem with expiry date format
            cookie.pop('expiry', None)  
            try:
                bot.add_cookie(cookie)
            except:
                print("Error adding cookie")
    
    #nameofvid = input(" Put the name of the video you want to upload (Ex: vid.mp4 or myshort.mp4 etc..) ---> ")
    nameofvid = filepath
    for i in range(1):
        
        print("Going to studio.youtube.com...")
        bot.get("https://studio.youtube.com")
        time.sleep(15)
        cookies = bot.get_cookies()

        with open('cookies.json', 'w') as cookies_file:
            json.dump(bot.get_cookies(), cookies_file)

        print("COOKIES")
        print(cookies)
        print('...done.')
        
        print("Clicking on upload icon...")
        try:
            time.sleep(3)
            upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
            upload_button.click()
            print('...done.')
        except Exception as e:
            print(f"Error: {e}")

        print("Sending upload sequence...")
        try:
            file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
            simp_path = '{}'.format(str(nameofvid))
            abs_path = os.path.abspath(simp_path)
            file_input.send_keys(abs_path)
            print('...done.')
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(7)

        print("Adding title...")
        try:
            time.sleep(3)
            title_box = bot.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
            title_box.clear()
            title_box.send_keys(title)
            print('...done.')
        except Exception as e:
            print(f"Error: {e}")

        print("Adding description...")
        try:
            time.sleep(3)
            description_box = bot.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
            description_box.clear()
            description_box.send_keys(description)
            print('...done.')
        except Exception as e:
            print(f"Error: {e}")


        print("Clicking Not For Kids button...")
        try:
            next_button = bot.find_element(By.XPATH, '//*[@id="audience"]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')
            next_button.click()
            time.sleep(1)
            print("clicked button")
        except Exception as e:
            print(f"Error: {e}")
            
        print("Clicking next buttons...")
        try:
            next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
            for i in range(3):
                next_button.click()
                time.sleep(1)
                print("clicked button")
            print("...done.")
        except Exception as e:
            print(f"Error: {e}")

        print("Clicking Make Video Public button...")
        try:
            done_button = bot.find_element(By.XPATH, '//*[@id="privacy-radios"]/tp-yt-paper-radio-button[3]')
            done_button.click()
            time.sleep(5)
            print("...done.")
        except Exception as e:
            print(f"Error: {e}")

        print("Clicking done button...")
        try:
            done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
            done_button.click()
            time.sleep(5)
            print("...done.")
        except Exception as e:
            print(f"Error: {e}")

        
        print(f"Successfully uploaded {filepath} to Youtube lol")

        

if __name__ == "__main__":
    upload_youtube_video("../generations/TEST_UPLOAD.mp4",title='Hello World', description="Hi hello world")

