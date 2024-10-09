from crawler import crawler
import argparse
import sys
import requests 

def check_link(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the status code indicates success (200-299)
    if response.ok:
        return
    else:

        print(f"The link {url} is offline. Status code: {response.status_code}")
        sys.exit(1)


def main():


    # Initialize the parser
    parser = argparse.ArgumentParser(description="Scrape a website and save the output")

    # Add arguments
    parser.add_argument("-u", "--url", required=True, help="URL of the website to scrape")
    parser.add_argument("-o", "--output",  help="Output file name")
    parser.add_argument("-e", "--external-links", action="store_true", help="Include external links")
    parser.add_argument("-i", "--images", action="store_true", help="Include images")

    # parse the arguments
    args = parser.parse_args()

    # Access the arguments
    url = args.url
    outfile_name = args.output
    
    #check_link(url)

    if outfile_name is not None:
        outfile_obj = open(outfile_name,'a+')
    else:
        outfile_obj = sys.stdout
   
    site_crawller = crawler(url,args.external_links)

    site_crawller._get_internal_links(include_images=args.images)

    for link in site_crawller.internal_links:
        outfile_obj.write(link+'\n')



    sys.exit(0)

if __name__ == '__main__':
    main()
