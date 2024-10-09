from os import fdopen
import sys
import re
import random


from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse



class crawler:
    def __init__(self,url,include_ext=False,impersonate='chrome'):
        self.url = url

        # TODO: add options for file extentions
        self.file_extentions = ['js','png','jpeg','jpg']
        self.include_ext = include_ext
        self.internal_links = set()
        self.external_links = set()
        self.impersonate = impersonate
        self.urlparsed = urlparse(self.url)
        self.domain = ".".join(self.urlparsed.netloc[1:])
        self.subdomain = self.urlparsed.netloc[0]

    def get_root_page(self,url1):
        res = requests.get(url1, impersonate=self.impersonate)

        if res.ok:
            return res.text
        else:
            raise ValueError("There was a problem in getting the root page")

    
    def get_root_soup(self):
        # Returns the parsable soup for the page specified in the url
        return BeautifulSoup(self.get_root_page(self.url),'html.parser')


    
    def get_all_image_links(self,soup):
        # Find all image tags (<img>) with a src attribute
        image_links = []
        for img_tag in soup.find_all('img', src=True):
            img_link = img_tag['src']
            if img_link.startswith('//'):
                image_links.append("https:"+img_link)
                continue

            if img_link.startswith('/'):
                root_url = self.urlparsed.scheme + "://" + self.urlparsed.netloc
                image_links.append(root_url + img_link)
                continue

        return image_links

    def _get_internal_links(self,url=None,include_images=False):
        if url is None:
            url = self.url

        html_text = self.get_root_page(url)
        soup = BeautifulSoup(html_text,'html.parser')

        if include_images:
            for img_link in self.get_all_image_links(soup):
                self.internal_links.add(img_link)

        if self.include_ext is False:
            for link in soup.find_all('a'):
                
                if 'href' in link.attrs:
                    inst_urlparsed = urlparse(link.attrs['href'])
                    if inst_urlparsed.scheme == '':
                        new_url = 'https://'+self.urlparsed.netloc+link.attrs['href']
                        self.internal_links.add(new_url)
                        if new_url not in self.internal_links:
                            self._get_internal_links(new_url)

                    elif inst_urlparsed.netloc == '':
                        new_url = 'https://'+self.urlparsed.netloc+link.attrs['href']
                        self.internal_links.add(new_url)
                        if new_url not in self.internal_links:
                            self._get_internal_links(new_url)
                        

                    elif inst_urlparsed.scheme == 'https' and self.domain in link.attrs['href']:
                        new_url = link.attrs['href']
                        self.internal_links.add(link.attrs['href'])
                        if new_url not in self.internal_links:
                            self._get_internal_links(new_url)

                    elif link.attrs['href'].startswith('/'):
                        new_url = 'https://'+self.urlparsed.netloc+link.attrs['href']
                        self.internal_links.add(new_url)
                        if new_url not in self.internal_links:
                            self._get_internal_links(new_url)
                    else:
                        new_url = link.attrs['href']
                        self.internal_links.add(new_url)
                        if new_url not in self.internal_links:
                            self._get_internal_links(new_url)

        else:
            for link in soup.find_all('a'):
                
                if 'href' in link.attrs:
                    inst_urlparsed = urlparse(link.attrs['href'])
                    if inst_urlparsed.scheme == '':
                        new_url = 'https://'+self.urlparsed.netloc+link.attrs['href']
                        self.internal_links.add(new_url)

                    elif inst_urlparsed.netloc == '':
                        self.internal_links.add('https://'+self.urlparsed.netloc+link.attrs['href'])
                        

                    elif inst_urlparsed.scheme == 'https' and self.domain in inst_urlparsed.netloc:
                        new_url = link.attrs['href']
                        self.internal_links.add(link.attrs['href'])
                    
                    elif inst_urlparsed.scheme == 'https':
                        new_url = link.attrs['href']
                        self.external_links.add(link.attrs['href'])
                        

                    if link.attrs['href'].startswith('/'):
                        self.internal_links.add('https://'+self.urlparsed.netloc+link.attrs['href'])
                
    

if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Australian_Football_League"
    url2 = "https://www.neduet.edu.pk/"
    url3 = "https://www.ssuet.edu.pk/"
    site1_craller = crawler(url,include_ext=False)
    site1_craller._get_internal_links() 
    
