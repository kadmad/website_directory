import xml.etree.ElementTree as ET
from django.urls import reverse
import re
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
    url = reverse('my_view_name', args=[item.slug])
    modified_time = item.created_at.strftime("%Y-%m-%d")
    image_url = item.image_url
    image_title = item.title

    add_url(url, modified_time, "daily", "1", title=image_title, image_url=image_url)

# Serialize the XML tree to a file
tree = ET.ElementTree(urlset)
tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
