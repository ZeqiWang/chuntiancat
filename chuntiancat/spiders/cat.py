# -*- coding: utf-8 -*-

import scrapy  # 导入scrapy包
import re
from bs4 import BeautifulSoup
from scrapy.http import Request  ##一个单独的request的模块，需要跟进URL的时候，需要用它
from chuntiancat.items import ChuntiancatItem

class CatSpider(scrapy.Spider):
    name = 'cat'
    allowed_domains = ['chuntiancat.com']
    start_urls = ['http://chuntiancat.com/']

    base_url = 'http://chuntiancat.com'
    p_base_url = 'http://chuntiancat.com/index_'
    t_base_url = ".html"

    # dir_path = 'G:\cat'  # 图片存放的路径

    # def start_requests(self):
    #     yield Request(self.base_url, self.parse)

    def parse(self, response):
        ####--------------------------------------------------------------------------------------
        for x in range(1, 21):

            if x == 1:
                content_href = self.base_url
            else:
                content_href = self.p_base_url +str(x)+self.t_base_url

            yield Request(str(content_href), self.getListInfo)

    def getListInfo(self, response):
        list_item = BeautifulSoup(response.text, 'lxml').find('div', id='img-container').find_all('div', class_='inner_wrapper_img')
        for item in list_item:
            href = item.find('a')['href']
            yield Request(self.base_url+href, self.getContentInfo)

    def getContentInfo(self, response):
        content_num = response.xpath("//h2/text()").extract()[0].encode("utf-8")
        reg = re.compile(r'\d+')
        numlist = reg.findall(content_num)
        index = len(numlist)
        num = numlist[index - 1]
        print (type(num))
        print (num)
        pic_url = response.url
        urllist = pic_url.split(".html")
        print (urllist)
        for x in range(1, int(num)+1):
            if x == 1:
                pic_url_info = response.url
            else:
                pic_url_info = urllist[0]+'_'+str(x)+'.html'
            print (pic_url_info)
            yield Request(pic_url_info, self.getImgSrc)

    def getImgSrc(self, response):

        # 获取图片的地址
        img_label = BeautifulSoup(response.text, "lxml").find('div',id='showImgWrap').find('div',class_='srcPic').find('img')



        src_info = img_label.get('src')
        print ("*" * 90)
        print (src_info)
        print ("*" * 90)
        mmjpgItem = ChuntiancatItem()
        mmjpgItem['src_info'] = src_info
        return mmjpgItem

