import requests
import time
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

max_retries = 5
def scrape_place(place_id):
    url = url_template.format(place_id)
    retries = 0
    while True:
        response = requests.get(url)
        if response.status_code == 200 or retries == max_retries:
            break
        retries += 1
        time.sleep(0.001)
    soup = BeautifulSoup(response.content, 'html.parser')

    name_tag = soup.find('h1')
    name = name_tag.text.strip() if name_tag else ''

    address_tag = soup.find('h4')
    address = address_tag.text.strip() if address_tag else ''

    contact_tag = soup.find('h3', text='Contact Information')
    contact = contact_tag.find_next_sibling('a').text.strip() if contact_tag else ''

    website_tag = soup.find('h3', text='Website')
    website = website_tag.find_next_sibling('a').text.strip() if website_tag else ''

    categories = []
    for category in soup.find_all('span', {'class': 'label'}):
        categories.append(category.text.strip())

    categories_str = ', '.join(categories)
    row = [url, name, address, contact, website, categories_str]

    return row

# Define the URL template and the range of IDs to loop through
url_template = 'https://www.places2play.org/place?id={}'
start_id = 1
end_id = 12835

# Define the CSV file and header row
csv_file = 'places.csv'
header_row = ['URL', 'Name', 'Address', 'Contact', 'Website', 'Categories']

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header_row)

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor() as executor:
        # Scrape the data for each place and update the progress bar
        for row in tqdm(executor.map(scrape_place, range(start_id, end_id + 1)), total = end_id - start_id + 1):
            writer.writerow(row)

print('Scraping completed.')