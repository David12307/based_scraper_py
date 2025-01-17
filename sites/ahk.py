from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
import urllib.parse

company = 'AHK'
url = 'https://www.ahkrumaenien.ro/ro/cariere/vino-in-echipa-noastra'

scraper = Scraper()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
}
scraper.set_headers(headers)
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='b-page-content b-page-content--main').find_all("section")

for job in jobs_elements:
    job_elem = job.find('div', class_='g-container')
    try:
        if job_elem:
            link_element = job.find('a', class_='rte_button--colored')
            if link_element:
                parsed = urllib.parse.urlparse(link_element['href'])
                if bool(parsed.netloc):  # The URL is absolute
                    job_link = link_element['href']
                else:  # The URL is relative
                    job_link = 'https://www.ahkrumaenien.ro' + link_element['href']
            else:
                job_link = None

            if job_link:
                jobs.append(create_job(
                    job_title=job.find('h3').text,
                    job_link=job_link,
                    city='Romania',
                    country='Romania',
                    company=company,
                ))
    except:
        continue

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/AHK-Logo.svg/512px-AHK-Logo.svg.png')
show_jobs(jobs)

