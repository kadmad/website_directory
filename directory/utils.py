import io
import os
import random
import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from PIL import Image, ImageChops, ImageDraw, ImageFont
import hashlib
from selenium import webdriver
from directory.models import Directory
import xml.etree.ElementTree as ET

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

    # Configure the Chrome web driver
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    # driver = webdriver.Chrome(options=options)


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

        # Open the screenshot with Pillow
        img = Image.open(screenshot_filename)
        draw = ImageDraw.Draw(img)
        font_size = 72
        font = ImageFont.truetype("arial.ttf", font_size)
            
        # Define the text to add
        text = "hcililongwe.in"

        # Define the position where you want to draw the text (x, y)
        text_position = (10, 800)

        # Define the text color
        text_color = (0, 0, 0)  # black

        # Add the text to the image
        white = (255, 255, 255)
        draw.rectangle((0, 700, 500, 1080), fill=white)
        draw.text(text_position, text, font=font, fill=text_color)
    
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


def ensure_unique_filename(folder_path, file_name):
    # Check if the file with the given name already exists in the folder
    if os.path.exists(os.path.join(folder_path, file_name)):
        base, ext = os.path.splitext(file_name)
        counter = 1
        while True:
            new_file_name = f"{base}_{counter}{ext}"
            if not os.path.exists(os.path.join(folder_path, new_file_name)):
                return new_file_name
            counter += 1
    return file_name


def are_images_similar(local_image, remote_image, threshold=95):
    try:

        # Check if the images have the same size
        if local_image.size != remote_image.size:
            return False

 # Convert the images to bytes
        buffer1 = io.BytesIO()
        local_image.save(buffer1, format="WebP")
        bytes1 = buffer1.getvalue()

        buffer2 = io.BytesIO()
        remote_image.save(buffer2, format="WebP")
        bytes2 = buffer2.getvalue()

        # Compare the bytes for equality
        if bytes1 == bytes2:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def erase_portion(image, output_path, erase_percentage_height, erase_percentage_width):
  

    # Get the image dimensions
    width, height = image.size

    # Calculate the dimensions of the portion to erase
    erase_width = int(width * erase_percentage_width / 100)
    erase_height = int(height * erase_percentage_height / 100)

    # Create a white rectangle to cover the specified portion
    white = (255, 255, 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, height - erase_height, erase_width, height), fill=white)

    font_size = 16
    font = ImageFont.truetype("arial.ttf", font_size)
        
    # Define the text to add
    text = "hcililongwe.in"

    # Define the position where you want to draw the text (x, y)
    text_position = (0, 230)

    # Define the text color
    text_color = (0, 0, 0)  # black

    # Add the text to the image
    draw.text(text_position, text, font=font, fill=text_color)
    # Save the modified image to the output path
    image.save(f"{output_path}")
    return output_path

    

def download_and_save_image(url, domain):
     # Define the folder and filename for the screenshot
    screenshot_folder = "media/snaps/"
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)  # Create the "snaps" folder if it doesn't exist

    base_file_path = f"{screenshot_folder}"
    try:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Open the local image using Pillow
            local_image = Image.open(f"{base_file_path}/sitelike.webp")

            # Open the remote image from the response content
            remote_image = Image.open(io.BytesIO(response.content))

            # Check if the images are at least 95% similar
            if not are_images_similar(local_image, remote_image, threshold=95):
                # Create the folder if it doesn't exist
                os.makedirs(base_file_path, exist_ok=True)
                file_path = erase_portion(remote_image, os.path.join(base_file_path, f"{domain.split('.')[0]}_small.webp"), 10, 25)

                return file_path
            else:
                return os.path.join(base_file_path, "default_site_image_thumbnail.webp")
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_domain_live(url):
    """check url is live and accessible or not"""
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print("check domain live exception:",e)
        return False
    
def fetch_live_domain_data(obj: Directory, url):
    """Fetching a live domain data"""
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract meta information
        # Title
        title = soup.find('title').text if soup.find('title') else 'No title found'

        # Description (using the "description" meta tag)
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else 'No description found'

        # Category (replace 'og:category' with the actual meta tag property name)
        category = soup.find('meta', attrs={'property': 'og:category'})
        category = category['content'] if category else 'other'

        file_path = capture_website_screenshot(url=url)
        # file_path = os.path.join("media/snaps", file_name)
        # Print the extracted information
        obj.title = title
        obj.description = description
        obj.category = category
        obj.image_url = file_path
        obj.save()
        return obj

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

from django.contrib.sitemaps import Sitemap
from directory.models import Directory

class DirectorySitemap(Sitemap):
    changefreq = 'daily'  # Set your preferred change frequency.
    priority = 1  # Set your preferred priority.

    def items(self):
        return Directory.objects.all()  # Adjust your queryset.

    def lastmod(self, obj):
        return obj.updated_at  # Use the last modified date of your blog post.

    def location(self, obj):
        return obj.get_absolute_url()  # Define a method to get the URL for each blog post.

    def image(self, obj):
        if obj.image:  # Check if there is an image associated with the blog post.
            return {
                'loc': obj.image_url,
                'title': obj.title,
            }
        else:
            return None

def fetch_site_like_data(directory: Directory):
    """Fetch website worth, followers and rank related data from sitelike"""
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    response = requests.get(f"https://www.sitelike.org/similar/{directory.domain}/", headers=headers)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        try:
            # Construct IDs for other elements
            description_element_id = f"MainContent_lblDescription"
            # title_element_id = f"MainContent_dl_lblDescription"
            file_path = f""
            # image_url_id = f"MainContent_dl_lblImage_{i}"
            moz_da_id = f"MainContent_lblMozDA"
            moz_rank_id = f"MainContent_lblMozRank"
            semrush_rank_title = f"Semrush Rank"
            worth_id = f"MainContent_dl_lblWorth"
            facebook_likes_id = f"MainContent_lblFacebookLikes"

            # Extract information for other elements
            # title = soup.find('span', {'id': title_element_id}).text.strip()
            # Check if the description element was found
            # Check if the description element was found
            site_description_element = soup.find('span', {'id': description_element_id})
            if site_description_element:
                site_description = site_description_element.text.strip()
            moz_da = 0
            moz_rank = 0
            semrush_rank = 0
            worth = 0
            facebook_likes = 0
            if soup.find('span', {'id': moz_da_id}):
                moz_da = soup.find('span', {'id': moz_da_id}).text.strip()
                moz_da = re.sub(r'[^0-9]', '', moz_da)
            if soup.find('span', {'id': moz_rank_id}):
                moz_rank = soup.find('span', {'id': moz_rank_id}).text.strip()
                moz_rank = re.sub(r'[^0-9]', '', moz_rank)

            if soup.find('span', {'title': semrush_rank_title}):
                semrush_rank = soup.find('span', {'title': semrush_rank_title}).text.strip()
                semrush_rank = re.sub(r'[^0-9]', '', semrush_rank)

            if soup.find('span', {'id': worth_id}):
                worth = soup.find('span', {'id': worth_id}).text.strip()
                worth = re.sub(r'[^0-9]', '', worth)

            if soup.find('span', {'id': facebook_likes_id}):
                facebook_likes = soup.find('span', {'id': facebook_likes_id}).text.strip()
                facebook_likes = re.sub(r'[^0-9]', '', facebook_likes)

            img_element = soup.find('img', {'id': "imgSiteThumb"})
            if img_element:
                src_url = img_element.get('src')
                file_path = download_and_save_image(src_url, directory.domain)
            else:
                directory = fetch_live_domain_data(directory, f"https://{directory.domain}")

            magical_worth = (int(facebook_likes) * random.randint(100,120))
            
            directory.description = site_description
            directory.image_url = file_path
            directory.da = moz_da
            directory.moz_rank = moz_rank
            directory.semrush_rank = semrush_rank
            directory.facebook_like = facebook_likes
            directory.worth = magical_worth
            directory.save()
                
        except Exception as e:
            print("exceptioin", e)