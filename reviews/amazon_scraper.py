import scrapy

class AmazonSpider(scrapy.Spider):

    name = "amazon"
    start_urls = [
        'https://www.amazon.com/Dell-Inspiron-Convertible-Touchscreen-Processor/dp/B00SGB4I1M',
    ]


    # def parse(self,response):
    #     page = response.url.split("/")[-2]
    #     filename = 'reviews-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % file)

    def parse(self, response):
        REVIEW_SELECTOR = '.review'
        TITLE_SELECTOR = '.review-title ::text'
        BODY_SELECTOR = '.a-expander-content ::text'
        STARS_SELECTOR = '.review-rating ::text'
        HELPFUL_SELECTOR = '.review-votes ::text'
        TIME_SELECTOR = '.review-date ::text'

        review_list = []

        for review_container in response.css(REVIEW_SELECTOR):
            review = {}
            review['summary'] = review_container.css(TITLE_SELECTOR).extract_first()
            review['body'] = review_container.css(BODY_SELECTOR).extract_first()
            review['overall'] = review_container.css(STARS_SELECTOR).extract_first()
            review['helpful'] = review_container.css(HELPFUL_SELECTOR).extract_first()
            review['review_time'] = review_container.css(TIME_SELECTOR).extract_first()


            review_list.append(review)

        return review_list

