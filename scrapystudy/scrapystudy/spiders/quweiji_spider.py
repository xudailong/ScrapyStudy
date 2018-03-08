# -*- coding: utf-8 -*-
# @Time    : 2018/1/21 17:44
# @Author  : 蛇崽
# @Email   : 643435675@QQ.com
# @File    : quwei.py(http://www.dsuu.cc/quwei-category/joke 趣味集)
import scrapy
import re


from scrapystudy.items import NewsItem

"""
这个类是scrapy的主类，主要是从网站上进行数据的解析，并使用items里面的类进行数据结构化
"""
class QuWeiJiSpider(scrapy.Spider):

    # spider 爬虫的名称
    name = 'quweiji'

    # 爬虫允许的域范围，防止跳转到其他网站
    allowed_domains = ['www.dsuu.cc']

    # 爬虫入口，也就是从这个网址开始进行爬取
    start_urls = ["http://www.dsuu.cc/quwei-category/joke"]

    # scrapy 默认的解析网页的方法，也就是第一次爬取网页，从这个方法返回数据
    def parse(self, response):
        # 这里是进行打印页面的内容
        # print('response',response.body)

        # 根据网站我们继续拼接每一页的url链接地址（爬取的页数是从1-300页）
        v_main_links = ['http://www.dsuu.cc/quwei-category/joke/page/{}'.format(n) for n in range(0, 300)] #300

        for v_link in v_main_links:
            # 这里是遍历每一个列表页的链接，进行爬取下一个地方的内容，回调是parse_v_list
            yield scrapy.Request(v_link, callback=self.parse_v_list)

    # 这里是进行列表页的解析
    def parse_v_list(self, response):

        # scrapy自带xpath的解析
        node_list = response.xpath("//*[@id='content']/div[@class='box_wrap ajz']/article[@class='post']")

        for v_node in node_list:
            newsItem = NewsItem()
            v_content_info = v_node.xpath("./div[@class='postbox pt']")
            title = v_content_info.xpath("./div[@class='exc nr']/header/h2/a/@title").extract_first()
            title_link = v_content_info.xpath("./div[@class='exc nr']/header/h2/a/@href").extract_first()
            v_keyword = v_content_info.xpath("./div[@class='exc nr']/p/text()").extract_first()
            v_footer_info = v_node.xpath("./footer[@class='entry-meta']")
            author = v_footer_info.xpath("./a[1]/text()").extract_first()
            release_time = v_footer_info.xpath("./span/text()").extract_first()

            newsItem['title'] = title if not None else ''
            newsItem['author'] = author if not None else ''
            newsItem['keywords'] = v_keyword if not None else ''
            newsItem['release_time'] = release_time if not None else ''

            # 找到列表页的每个item的链接，进行详情页的链接解析
            if title_link:
                # meta为带着参数过去，callback 回调到具体每一篇文章的详情页内容
                yield scrapy.Request(title_link, callback=self.parse_v_detail, meta={'newsItem': newsItem})

    # 这里是解析详情页内容的具体操作
    def parse_v_detail(self, response):
        newsItem = response.meta['newsItem']
        content = re.findall(r'<div class="content">(.*?)</div>', response.body.decode("utf-8"), re.S)[0]
        # 去掉这张图片
        content = re.sub(r'src="http://www.dsuu.cc/wp-content/themes/dsuu/images/grey.gif"', '', content)
        content = re.sub(r'<img.*data-original.*<noscript>','',content)
        newsItem['body'] = content
        newsItem['orginal_url'] = response.url
        yield newsItem
