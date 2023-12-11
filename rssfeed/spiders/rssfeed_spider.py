import scrapy
import re
from rssfeed.items import RssfeedItem


class RssfeedSpiderSpider(scrapy.Spider):
    name = "rssfeed_spider"

    def start_requests(self):
        url = "https://prnewswire.mediaroom.com/rss?rsspage=29533"
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        await page.screenshot(path="main_page.png")

        # Get the iframe handle
        iframe_handle = await page.wait_for_selector(
            '//*[@id="wd_featurebox-social_5"]/div/iframe'
            )
        iframe = await iframe_handle.content_frame()

        # Query for the element using CSS selector
        data_elements_1 = await iframe.query_selector_all(
            '._5pbx.userContent._3576'
            )

        # Query for all elements with the second class "_3dp _29k"
        data_elements_2 = await iframe.query_selector_all('._3dp._29k')

        # Query for all elements with the third class "mtm"
        data_elements_3 = await iframe.query_selector_all('.mtm')

        if len(data_elements_1) > 0:
            for data_element_1, data_element_2, data_element_3 in \
                zip(
                    data_elements_1,
                    data_elements_2,
                    data_elements_3):
                # Extract text content from each element
                data_text_1 = await data_element_1.inner_text()
                data_text_2 = await data_element_2.inner_text()
                # Extract text content from each element
                # Extract the src attribute from the image within the element
                # with class "mtm"
                image_element = await data_element_3.query_selector('img')
                image_src = await image_element.get_attribute('src')
                # data_text = await data_element.inner_text()
                links = self.extract_links_from_text(data_text_1)
                # Remove links from data_text_1
                cleaned_text_1 = self.remove_links_from_text(data_text_1)
                book_data = RssfeedItem(
                    links=links,
                    title=data_text_2,
                    text=cleaned_text_1,
                    image_url=image_src,
                )

                # Yield the item
                yield book_data
        else:
            print("Element not found")

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    def extract_links_from_text(self, text):
        pattern = (
            r'http[s]?://'
            r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
            r'|[!*\\(\\),]'
            r'|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            )
        return re.findall(pattern, text)

    def remove_links_from_text(self, text):
        pattern = (
            r'http[s]?://'
            r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
            r'|[!*\\(\\),]'
            r'|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            )
        return re.sub(pattern, '', text)
