from bs4 import BeautifulSoup
import requests
import json
import csv

url = 'https://www.trustpilot.com/review/www.kfc.com'

csv_file = open('cms_scrapte.csv', 'w')

csv_wirter = csv.writer(csv_file)
csv_wirter.writerow(['name', 'location', 'rating',
                     'date', 'headline', 'summary'])


def get_data(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def get_next_page_link(soup):
    page = soup.find('nav', {'class': 'pagination-container AjaxPager'})
    if page.find('a', {'class': 'button button--primary next-page'}):
        url = 'https://www.trustpilot.com' + \
            str(page.find('a', {'class': 'next-page'})['href'])
        return url
    else:
        return


while True:
    soup = get_data(url)
    url = get_next_page_link(soup)
    print(url)
    for article in soup.find_all('article'):
        name = article.find(
            'div', {'class': 'consumer-information__name'}).text
        # print(name)

        location = article.find(
            'div', {'class': 'consumer-information__location'}).span.text
        # print(location)

        section = article.find('section')

        rating = section.find(
            'div', {'class': 'star-rating star-rating--medium'}).img['alt']
        # print(rating)

        date_json = section.find('script').string
        date = json.loads(date_json)['publishedDate']
        # print(date)

        headline = section.h2.a.text
        # print(headline)

        summary = section.find('p', {'class': 'review-content__text'}).text
        # print(summary)

        print()

        csv_wirter.writerow([name, location, rating, date, headline, summary])
    if not url:
        csv_file.close()
        break
