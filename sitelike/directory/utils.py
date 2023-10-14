import os
from selenium import webdriver
from PIL import Image

def capture_website_screenshot(url):
    # Extract the domain name from the URL
    domain = url.split("//")[-1].split("/")[0]
    domain = domain.replace(".", "_")  # Replace dots with underscores
    domain = domain.rstrip("_")  # Remove trailing underscores

    # Define the folder and filename for the screenshot
    screenshot_folder = "media/snaps"
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)  # Create the "snaps" folder if it doesn't exist

    base_filename = f"{screenshot_folder}/{domain}"
    screenshot_filename = f"{base_filename}.png"

    # Check if a file with the same name already exists
    counter = 1
    while os.path.exists(screenshot_filename):
        screenshot_filename = f"{base_filename}_{counter}.png"
        counter += 1

    # # Configure the Chrome web driver
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    # driver = webdriver.Chrome(options=options)

    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    chrome_options.add_argument("--disable-infobars")  # Disable infobars (deprecated)
    chrome_options.add_argument("--start-maximized")  # Start browser in maximized mode
    

    # Set custom User-Agent header
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.1234.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Take a screenshot
        driver.save_screenshot(screenshot_filename)
        print('screenshot_filename: ', screenshot_filename)

        # Open the screenshot with Pillow
        img = Image.open(screenshot_filename)
        print('img: ', img)

        # Resize to 450x450
        img.thumbnail((450, 450))

        # Save as WebP format
        thumbnail_filename = f"{base_filename}_thumbnail.webp"
        img.save(thumbnail_filename, "webp")

    finally:
        # Close the web driver
        driver.quit()

        # Delete the PNG screenshot
        if os.path.exists(screenshot_filename):
            os.remove(screenshot_filename)

    # Return the relative path of the saved thumbnail
    return thumbnail_filename

