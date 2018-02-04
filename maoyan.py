# -*- coding: utf-8 -*-
# date: 2018-01-27
# author:King
# vision:0.01

import  requests
from requests.exceptions import  RequestException
import  re
import json
from multiprocessing import Pool

def maoyan(url):
    try:
        response = requests.get(url)
        if response.status_code ==200: ## 从类没有想到过if else 可以这样写
             return response.text
        return  None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?<a.*?image-link.*?title=(.*?).*?board-img.*?src="(.*?)"></a>'
        +'.*?star">(.*?)</p><p class="releasetime">(.*?)</p>'
        +'integer">(.*?).*?fraction">(d)</i></p>',re.S )
    items = re.match(pattern,html)
    for item in items:
        yield {
            'image':item[0],
            'title':item[1],
            'star':item[2],
            'time':item[3]
            'score':item[4]+item[5]
        }
def write_to_file(content):
    with open("resule.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        # json.dumps 将 Python 对象编码成 JSON 字符串

def main(offset):
    url ='http://maoyan.com/board/4?offset'+str(offset)
    html= maoyan(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__=='__main__':
    # 下面是多进程的一般写法
    pool =Pool()
    pool.map(main(),[i*10 for i in range(10)])
    pool.close()
    pool.join()