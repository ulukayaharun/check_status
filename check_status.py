from sendmail import sendmail
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def check_status(website_url):
    # Base site URL
    base_url = f"https://{website_url}"

    # A dictionary to collect URLs
    urls = {}
    # Prevent sending multiple requests to the same site
    checked_urls=set()
    
    # request to the base site
    response = requests.get(base_url)
    if response.status_code == 200:
        # Parsing the content of the home page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links and check status codes
        for link in soup.find_all('a', href=True):
            url = urljoin(base_url, link['href'])
            if urlparse(url).scheme in ['http', 'https'] and url not in checked_urls:
                try:
                    # Status_code control for all URL
                    link_response = requests.get(url)
                    # If status_code not 200, add to dictionary
                    if link_response.status_code != 200:
                        urls[url]=link_response.status_code
                        print(f"{url} : {link_response.status_code}")

                except requests.RequestException as e:
                    print(f"An exception in link control: {e}")
                finally:
                    checked_urls.add(url)
    return urls

if __name__=="__main__":
    url_posta = check_status("github.com")
    recipients = ["example@mail.com"]
    if url_posta:
        sendmail(recipients, str(url_posta))
    else:
        print("no problem")

