from bs4 import BeautifulSoup
import requests
import re

# 각 크롤링 결과 저장하기 위한 리스트 선언
link_text = []
content_url = []
content_text = []
result = {}

def cleaning(temp):
    temp = re.sub('<.+?>', '', temp, 0).strip()
    temp = re.sub(',', ' ', temp, 0).strip()
    temp = re.sub('\n', '', temp, 0).strip()
    temp = re.sub('\u200b', '', temp, 0).strip()
    temp = re.sub('가벼운글쓰기툴퀵에디터가오픈했어요!', '', temp, 0).strip()
    temp = re.sub('가벼운툴퀵에디터가오픈했어요!', '', temp, 0).strip()
    temp = re.sub('가벼운 툴 퀵에디터가 오픈했어요!', '', temp, 0).strip()
    temp = re.sub('이 달의 결심, 실천일기를 퀵에디터로 기록해보세요.', '', temp, 0).strip()
    temp = re.sub('오늘 있었던 일을 퀵에디터로 기록해보세요.', '', temp, 0).strip()
    temp = re.sub('BGM플레이어를 이용하시려면 여기를 참고하여 Adobe Flash Plugin을 활성화해주세요.', '', temp, 0).strip()
    temp = re.sub('지금 떠오른 생각을 퀵에디터로 메모해보세요.', '', temp, 0).strip()
    temp = re.sub('다시 읽고 싶은 링크를 퀵에디터로 남겨보세요.', '', temp, 0).strip()
    temp = re.sub('이 달의 결심  실천일기를 퀵에디터로 기록해보세요.', '', temp, 0).strip()
    temp = re.sub('오늘 찍은 사진을 퀵에디터로 남겨보세요.', '', temp, 0).strip()
    temp = re.sub('로그인', '', temp, 0).strip()
    temp = re.sub('글쓰기', '', temp, 0).strip()
    temp = re.sub('이전', '', temp, 0).strip()
    temp = re.sub('재생', '', temp, 0).strip()
    temp = re.sub('다음', '', temp, 0).strip()
    temp = re.sub('정지', '', temp, 0).strip()
    temp = re.sub('SET', '', temp, 0).strip()
    temp = re.sub('LIST', '', temp, 0).strip()
    temp = re.sub('레이어 닫기', '', temp, 0).strip()
    temp = re.sub('블로그 메뉴', '', temp, 0).strip()
    temp = re.sub('공지 목록', '', temp, 0).strip()
    temp = re.sub('공지글', '', temp, 0).strip()
    temp = re.sub('\xa0', '', temp, 0).strip()
    temp = re.sub('\t', '', temp, 0).strip()
    return temp

def crawler(maxpage, keyword):
    page = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지
    while page <= maxpage_t:

        url = "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=blog.naver.com&post_blogurl_without=&query=" + keyword + "&sm=tab_pge&srchby=all&st=sim&where=post&start=" + str(page)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 링크  추출
        atags = soup.select('._sp_each_title')
        for atag in atags:
            link_text.append(atag['href'])  # 링크주소
            content_link = atag['href']
            sub_response = requests.get(content_link)
            sub_html = sub_response.text
            sub_soup = BeautifulSoup(sub_html, 'html.parser') # 링크 내 본문 주소
            temp_link = sub_soup.find('iframe').get('src')
            temp_url = 'https://blog.naver.com' + temp_link
            content_url.append(temp_url)
        page += 10 # 페이지 증가

    # 본문 추출
    for link in content_url:
        content_response = requests.get(link)
        content_html = content_response.text
        content_soup = BeautifulSoup(content_html, 'html.parser')
        temp = str(content_soup.select('p'))
        string = cleaning(temp)
        content_text.append(string)

    # txt 저장
    f = open('crawling_data.txt', 'w', encoding='utf8')
    for i in content_text:
        f.write(i)
        f.write('\n\n')
    f.close()


def main():
    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
    keyword = input("검색어 입력: ")
    crawler(maxpage, keyword)


main()












