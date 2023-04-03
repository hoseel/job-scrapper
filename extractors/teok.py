import requests
from bs4 import BeautifulSoup


def extract_teok_jobs(keyword):
    results = []
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})

    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all('tr', class_="job")

        for job_section in jobs:
            job_posts = job_section.find_all('td', class_="company")
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[0]
                link = anchor['href']
                title = anchor.find("h2")

                organization = post.find_all('span', class_="companyLink")
                orga = organization[0]
                company = orga.find('h3')
                location = post.find_all('div', class_="location")[0]

                if company:
                    company = company.string.strip()
                if title:
                    title = title.string.strip()
                if location:
                    location = location.string

                job_data = {
                    'link': f"https://remoteok.com{link}",
                    'company': company.replace(",", " "),
                    'location': location.replace(",", " "),
                    'position': title,
                }
                results.append(job_data)
    return results