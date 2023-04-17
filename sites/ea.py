from scraper_peviitor import Scraper, Rules, loadingData
import uuid

import re

scraper = Scraper()
rules = Rules(scraper)
regex  = re.compile(r"search-results-(.*?)-bodyEl")

pageNumber = 1
foundedJobs = True

finalJobs = list()

while foundedJobs:
    url = f"https://ea.gr8people.com/jobs?page={pageNumber}&geo_location=ChIJw3aJlSb_sUARlLEEqJJP74Q"

    doom = scraper.post(url).text
    scraper.soup = doom
    
    elementId = re.findall(regex, doom)[0]
    jobsContainer = rules.getTag("tbody", {"id": f"search-results-{elementId}-bodyEl"})
    jobs = jobsContainer.find_all("tr")

    foundedJobs = len(jobs) > 0

    for job in jobs:
        id = str(uuid.uuid4())
        job_title = job.find_all("td")[1].text.strip()
        job_link = job.find("a").get("href")
        company = "Electronic Arts"
        country = "Romania"
        city = "Romania"

        print(job_title + " -> " + city)

        finalJobs.append(
            {
                "id": id,
                "job_title": job_title,
                "job_link": job_link,
                "company": company,
                "country": country,
                "city": city,
            })

    pageNumber += 1

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Electronic Arts")