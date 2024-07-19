from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def navigate_to_youtube_studio():
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    
    # Specify the path to chromedriver
    service = Service(executable_path="./chromedriver")
    
    # Initialize the driver with the specified service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Navigate to YouTube Studio
    driver.get("https://studio.youtube.com")
    
    # Optionally, print the page title to verify successful navigation
    print("Navigated to:", driver.title)
    
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    navigate_to_youtube_studio()
