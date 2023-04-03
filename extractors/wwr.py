from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    results = []
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    request = get(url)

    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all('section', class_="jobs")

        for job_section in jobs:
            job_posts = job_section.find_all("li")
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[1]
                link = anchor["href"]
                company, kind, location = anchor.find_all('span',
                                                          class_="company")
                position = anchor.find('span', class_="title")

                if company:
                    company = company.string.strip()
                if position:
                    position = position.string.strip()
                if location:
                    location = location.string

                job_data = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.replace(",", " "),
                    'location': location,
                    'position': position.replace(",", " ")
                }
                results.append(job_data)
    return results
