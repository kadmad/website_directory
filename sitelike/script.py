import re
from bs4 import BeautifulSoup
from django.conf import settings
import requests
import os
import django
from urllib.parse import urlparse, parse_qs
# Change to your Django project's directory
project_directory = 'C:\\Users\\Khushbu\\PycharmProjects\\pythonProject\\django-sitelike'
os.chdir(project_directory)
settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sitelike.settings")
django.setup()
from directory.models import Directory
from directory.utils import capture_website_screenshot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
response = requests.get("https://www.sitelike.org/top-websites.aspx", headers=headers)

if response.status_code == 200:
    page_content = response.content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Initialize a list to store the extracted information
    site_info = []

    # Loop through the IDs (0 to 99)
    for i in range(100):  # IDs from 0 to 99

        # Extract site description using the element ID
        

        # Construct IDs for other elements
        description_element_id = f"MainContent_dl_lblWiki_{i}"
        title_element_id = f"MainContent_dl_lblDescription_{i}"

        image_url_id = f"MainContent_dl_lblImage_{i}"
        moz_da_id = f"MainContent_dl_lblMozDA_{i}"
        moz_rank_id = f"MainContent_dl_lblMozRank_{i}"
        semrush_rank_id = f"MainContent_dl_lblSemRushRank_{i}"
        worth_id = f"MainContent_dl_lblWorth_{i}"
        facebook_likes_id = f"MainContent_dl_lblFacebookLikes_{i}"

        # Extract information for other elements
        title = soup.find('span', {'id': title_element_id}).text.strip()
        # Check if the description element was found
        # Check if the description element was found
        site_description_element = soup.find('span', {'id': description_element_id})
        if site_description_element:
            site_description = site_description_element.text.strip()

            # Find the parent div element of the description element
            parent_div = site_description_element.find_parent('div', class_='col-md-8 col-xs-12')

            # Find the anchor tag within the parent div
            anchor_tag = parent_div.find('a', {'class': 'btn btn-link btn-lg'})

            # Check if the anchor tag was found
            if anchor_tag:
                # Get the URL from the href attribute
                anchor_url = anchor_tag.get('href')
                domain = anchor_url.split("/")[-2].strip()
                try:
                    file_path = capture_website_screenshot(f"https://{domain}")
                except:
                    file_path = ""
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

        if soup.find('span', {'id': semrush_rank_id}):
            semrush_rank = soup.find('span', {'id': semrush_rank_id}).text.strip()
            semrush_rank = re.sub(r'[^0-9]', '', semrush_rank)

        if soup.find('span', {'id': worth_id}):
            worth = soup.find('span', {'id': worth_id}).text.strip()
            worth = re.sub(r'[^0-9]', '', worth)

        if soup.find('span', {'id': facebook_likes_id}):
            facebook_likes = soup.find('span', {'id': facebook_likes_id}).text.strip()
            facebook_likes = re.sub(r'[^0-9]', '', facebook_likes)

       
        # Append the extracted information to the site_info list as a dictionary
        site_info.append({
            "description": site_description,
            "title": title,
            "domain": domain,
            "image_url": file_path,
            "moz_da": moz_da,
            "moz_rank": moz_rank,
            "semrush_rank": semrush_rank,
            "worth": worth,
            "facebook_likes": facebook_likes,
        })
        Directory.objects.create(**{
            "description": site_description,
            "title": title,
            "domain": domain,
            "image_url": file_path,
            "da": moz_da,
            "moz_rank": moz_rank,
            "semrush_rank": semrush_rank,
            "worth": worth,
            "facebook_like": facebook_likes,
        })

# Directory.objects.bulk_create([Directory(**data) for data in site_info])
print("------------completed--------------------")