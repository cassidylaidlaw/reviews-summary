import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time

from reviews.data import Review

def scrape_reviews_from_url(url):
    """
    Given the URL of an Amazon product page, scrapes the reviews of that
    product and returns them as a list.
    """
    
    reviews = []
    
    product_page = requests.get(url)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    next_link = product_soup.find(id='dp-summary-see-all-reviews')['href']
    while next_link is not None:
        time.sleep(random.random())
        next_link = 'https://www.amazon.com' + next_link
        reviews_page = requests.get(next_link)
        reviews_soup = BeautifulSoup(reviews_page.content, 'html.parser')
        for review_container in reviews_soup.find_all(class_='review'):
            summary = review_container.find(class_='review-title').get_text()
            body = review_container.find(class_='review-text').get_text()
            overall = float(review_container.find(class_='review-rating')
                            .get_text()[:3])
            
            try:
                helpful_text = review_container.find(class_='review-votes').get_text()
                helpful_num = helpful_text.strip().split()[0]
                if helpful_num == 'One':
                    helpful_num = 1
                else:
                    helpful_num = int(helpful_num)
                helpful = (helpful_num, helpful_num)
            except AttributeError: # If there's no helpful text
                helpful = (0, 0)
                
            date_text = review_container.find(class_='review-date').get_text()
            date_text = date_text.strip()[3:]
            review_date = datetime.strptime(date_text, '%B %d, %Y')
            
            reviews.append(Review(body, summary, overall, helpful,
                                  review_date))
            
        next_buttons = reviews_soup.select('#cm_cr-pagination_bar .a-last')
        if len(next_buttons) > 0:
            next_a = next_buttons[0].find('a')
            if next_a is not None:
                next_link = next_a['href']
            else:
                next_link = None
        else:
            next_link = None
            
    return reviews
