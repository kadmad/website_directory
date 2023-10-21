import random
import re
from bs4 import BeautifulSoup
from django.views import View
import requests
from directory.models import Directory
from django.core.management.base import BaseCommand
from contextlib import suppress

from directory.utils import download_and_save_image


class Command(BaseCommand):
    help = 'Scrapping management command'
    def handle(self, *args, **options):
        """To scrap the data"""
        print("---------------scrapping-runned----------------")
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        for j in range(1,2):
            print(f"------------------------Page NO. {j} -------------------------------")
            response = requests.get(f"https://www.sitelike.org/top-websites.aspx?p={j}", headers=headers)
            if response.status_code == 200:
                page_content = response.content
                soup = BeautifulSoup(page_content, 'html.parser')

                # Initialize a list to store the extracted information
                site_info = []
                try:
                    # Loop through the IDs (0 to 99)
                    for i in range(98, 100):  # IDs from 0 to 99
                        print(f"------------------------Website No. {(j-1)*100 + i+1} -------------------------------")

                        # Construct IDs for other elements
                        description_element_id = f"MainContent_dl_lblWiki_{i}"
                        title_element_id = f"MainContent_dl_lblDescription_{i}"
                        file_path = f""
                        # image_url_id = f"MainContent_dl_lblImage_{i}"
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
                            file_path = ""
                            if anchor_tag:
                                # Get the URL from the href attribute
                                anchor_url = anchor_tag.get('href')
                                domain = anchor_url.split("/")[-2].strip()
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

                        img_element = soup.find('img', {'title': domain, 'class': "WebsiteImageSmall"})
                        if img_element:
                            src_url = img_element.get('src')
                            file_path = download_and_save_image(src_url, domain)
                            
                        print({
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
                        # Append the extracted information to the site_info list as a dictionary
                        site_info.append({
                            "description": site_description,
                            "title": title,
                            "domain": domain,
                            "image_url": file_path,
                            "moz_da": min(int(moz_da)+1, 100),
                            "moz_rank": min(int(moz_rank)+1, 100),
                            "semrush_rank": int(semrush_rank)+random.randint(1,10),
                            "worth": int(worth)+random.randint(1,10),
                            "facebook_likes": int(facebook_likes)+random.randint(1,10),
                        })
                        directory_obj_qs = Directory.objects.filter(domain=domain)
                        if not directory_obj_qs:
                            print(f"----------try create, {i+1}------------")
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
                            print("----------created------------")
                        else:
                            directory_obj_qs.update(**{
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

                 
                except Exception as e:
                    print("exceptioin", e)

class GenerateSitemap(View):
    def get(self):
        """Generate Sitemap"""
        import xml.etree.ElementTree as ET
        from django.urls import reverse
        # Create an XML sitemap root element
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        image_namespace = "http://www.google.com/schemas/sitemap-image/1.1"

        # Function to add a URL with optional image data
        def add_url(url, lastmod, changefreq, priority, title=None, image_url=None):
            url_elem = ET.SubElement(urlset, "url")
            loc_elem = ET.SubElement(url_elem, "loc")
            loc_elem.text = url
            lastmod_elem = ET.SubElement(url_elem, "lastmod")
            lastmod_elem.text = lastmod
            changefreq_elem = ET.SubElement(url_elem, "changefreq")
            changefreq_elem.text = changefreq
            priority_elem = ET.SubElement(url_elem, "priority")
            priority_elem.text = priority
            
            if title and image_url:
                image_elem = ET.SubElement(url_elem, f"{{{image_namespace}}}image")
                image_loc_elem = ET.SubElement(image_elem, f"{{{image_namespace}}}loc")
                image_loc_elem.text = image_url
                image_title_elem = ET.SubElement(image_elem, f"{{{image_namespace}}}title")
                image_title_elem.text = title

        # Retrieve data from Django model and create URLs with optional image data
        # Replace 'MyModel' with your actual model name and adapt the query accordingly
        queryset = Directory.objects.all()

        for item in queryset:
            url = reverse('website-detail', args=[item.pk])
            modified_time = item.created_at.strftime("%Y-%m-%d")
            image_url = item.image_url
            image_title = item.title

            add_url(url, modified_time, "daily", "1", title=image_title, image_url=image_url)

        # Serialize the XML tree to a file
        tree = ET.ElementTree(urlset)
        tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)