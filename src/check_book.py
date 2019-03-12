# -*-coding:utf-8 -*-
import requests
import json
import re


url = "http://210.35.251.243/opac/ajax_isbn_marc_no.php?marc_no=2b71564670566f6434717974564d776745314d3645773d3d&rdm=0.061923616269299764&isbn=978-7-115-43559-0"

def query_books_remainder(url):
    '''
    return totalNum(int) , remainderNum(int)   
    '''
    info = requests.get(url)
    book = json.loads(info.text)
    total = re.search("</b>\d+<br>",book.get("lendAvl")).group()
    total = re.search("\d+",total).group()
    remainder = re.search("\d+$",book.get("lendAvl")).group()
        
    print("totalis {} and remainder is {}".format(total, remainder))
    totalNum = int(total)  
    remainderNum = int(remainder)
    return totalNum , remainderNum

def main():
    query_books_remainder(url)

if __name__ == "__main__":
    main()
