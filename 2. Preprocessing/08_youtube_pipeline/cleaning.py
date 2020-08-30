#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 시간 관리 및 데이터 정제
from datetime import datetime
import time
import re

# 데이터 관리
import numpy as np
import pandas as pd
import sqlite3

# 유튜브 정보 추출
from apiclient.discovery import build
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

# 웹 정보 수집
import urllib
import requests
from bs4 import BeautifulSoup


# In[ ]:


def df_cleaning(DataFrame, cleaning_function):
    
    copy = DataFrame.copy()
    
    copy.dropna(axis=0, inplace=True)
    copy.reset_index(drop=True, inplace=True)
    
    cleaned_description = [cleaning_function(element) for element in copy['description']]
    copy['cleaned_description'] = cleaned_description
    
    copy.dropna(axis=0, inplace=True)
    copy.reset_index(drop=True, inplace=True)
    
    # 본문의 string 길이가 250 이하인 데이터만 남기기 => 요약을 위해서 어느정도 길이가 있어야 된다고 판단
    copy = copy.loc[copy['cleaned_description'].str.len() > 250]
    copy.reset_index(drop=True, inplace=True)
    
    return copy


# In[ ]:


def ytn_description_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'(취재기자\s?:\s?\w{1,})?', '', text)
    text = re.sub(r'(촬영기자\s?:\s?\w{1,})?', '', text)
    text = re.sub(r'(그래픽\s?:\s?\w{1,})?', '', text)
    text = re.sub(r'(자막뉴스\s?:\s?\w{1,})?', '', text)
    text = re.sub(r'\[앵커\]|\[기자\]', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\.\.\. \(중략\)', ' ', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    
    text = re.sub(r"■ 진행 : \w{1,} 앵커(, \w{1,} 앵커)?", '', text)
    text = re.sub(r"■ 출연 : \w{1,} 기자(, \w{1,} 기자)?", '', text)
    text = re.sub(r"■ 출연 : \w{1,} 기상 캐스터(, \w{1,} 기상 캐스터)?", '', text)
    text = re.sub(r"■ 출연 : \w{1,} / 기상청 통보관(, \w{1,} / 기상청 통보관)?", '', text)
    text = re.sub(r"■ 출연 : \w{1,} / 한국기상산업협회 본부장(, \w{1,} / 한국기상산업협회 본부장)?", '', text)
    text = re.sub(r"■ 출연 : \w{1,} / 케이웨더 예보센터장(, \w{1,} / 케이웨더 예보센터장)?", '', text)
    text = re.sub(r"\* 아래 텍스트는 실제 방송 내용과 차이가 있을 수 있으니 보다 정확한 내용은 방송로 확인하시기 바랍니다.",
                  '', text)
    text = re.sub(r"\* 아래 텍스트는 실제 방송 내용과 차이가 있을 수 있으니 보다 정확한 내용은 방송으로 확인하시기 바랍니다.",
                  '', text)
    text = re.sub(r"(■ 출연 : )", '', text)
    
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
    text = text.split('▶')[0].split('※')[0]
    
    # []로 쌓여있는 문자열 제거
#     text = re.sub(r'\[[\S\s]*?\]', '', text)
    text = re.sub(r'\([\S\s]*?\)', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 특수문자, 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'’', '', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def yonhab_description_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'\b([a-z1-9]+(?:[.@]?[a-z]+)+)\b', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
    text = text.split('▣')[0]
    
    # []로 쌓여있는 문자열 제거
#     text = re.sub(r'\[[\S\s]*?\]', '', text)
    text = re.sub(r'\([\S\s]*?\)', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 특수문자, 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'▶', '', text)
    text = re.sub(r'’', '', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def channel_a_description_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'■ 방송 : 채널A 뉴스A 라이브', '', text)
    text = re.sub(r'■ 방송일 : 2020년 \d{1,}월 \d{1,}일', '', text)
    text = re.sub(r'■ 진행 : [가-힣]{1,} 앵커(, [가-힣]{1,} 앵커)?', '', text)
    text = re.sub(r'■ 출연 : [가-힣]{1,}', '', text)
    text = re.sub(r'--------------------------------------------', '', text)
    text = re.sub(r'\* 위 텍스트는 실제 토크 내용의 일부분입니다. 전체 토크 내용은 동영상으로 확인하시기 바랍니다.', '', text)
    text = re.sub(r'\&nbsp\;', '', text)
    text = re.sub(r'\b([a-z1-9]+(?:[.@]?[a-z]+)+)\b', '', text)
    text = re.sub(r'\bhttps?://\w+(?:[.]?\w+)+\b', '', text)
    text = re.sub(r'(영상편집 : \w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(영상취재 : \w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'\/', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r"’|‘|“|”", ' ', text)
    text = re.sub(r"\&", ' ', text)
    text = re.sub(r'\u200b', '', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    text = re.sub(r"(Q.)", '', text)
    text = re.sub(r"(\+α)", ' 이상', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # 문단을 나누는 특수문자 뒤의 문자열은 다 제거
    text = text.split('▷')[0].split('※')[0]
    
    # [], ()로 쌓여있는 문자열 제거
#     text = re.sub(r'\[[\S\s]*?\]', '', text)
    text = re.sub(r'\([\S\s]*?\)', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 문자열이 전부 영어면 제거 => 한국어로 되어있으면 '다'를 포함하지 않는 글은 없음
    if '다' not in text:
        text = re.sub(r'[^가-힣]', '', text)
    
    # 띄어쓰기 중복으로 되어 있는 부분 정리
    
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def mbn_description_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'\b([a-z1-9]+(?:[.@]?[a-z]+)+)\b', '', text)
    text = re.sub(r'\/', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r'\u200b', '', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(cm)', '센치미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
    text = text.split('☞')[0].split('📢')[0]
    
    # [], ()로 쌓여있는 문자열 제거
#     text = re.sub(r'\[[\S\s]*?\]', '', text)
    text = re.sub(r'\([\S\s]*?\)', '', text)
    text = re.sub(r'\【[\S\s]*?\】', '', text)
    
    text = re.sub(r"(▶ 스탠딩 \: [가-힣]{1,4}  기자)", '', text)
    text = re.sub(r"(▶ 인터뷰 \: [가-힣]{1,4})", '', text)
    text = re.sub(r"(▶ 인터뷰 \: [가-힣]{1,4})", '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 문자열이 전부 영어면 제거 => 한국어로 되어있으면 '다'를 포함하지 않는 글은 없음
    if '다' not in text:
        text = re.sub(r'[^가-힣]', '', text)
    
    # 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'「|」', ' ', text)
    text = re.sub(r'『|』', ' ', text)
    text = re.sub(r'▶', ' ', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def kbs_description_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'(촬영기자:\w{1,}·\w{1,})?', '', text)
    text = re.sub(r'(촬영기자:\w{1,}( \w{1,})?( \w{1,})?( \w{1,})?( \w{1,})?)?', '', text)
    text = re.sub(r'(촬영감독:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(항공촬영:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(항공취재:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(영상 편집:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(영상편집:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(영상편집 : \w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(촬영기자 \w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(촬영:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(편집:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'(그래픽:\w{1,}( \w{1,})?)?', '', text)
    text = re.sub(r'\/', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r'\u200b', '', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
    text = text.split('#')[0].split('▣')[0].split('▶')[0]
    
    # [], ()로 쌓여있는 문자열 제거
#     text = re.sub(r'\[[\S\s]*?\]', '', text)
    text = re.sub(r'\([\S\s]*?\)', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 문자열이 전부 영어면 제거 => 한국어로 되어있으면 '다'를 포함하지 않는 글은 없음
    if '다' not in text:
        text = re.sub(r'[^가-힣]', '', text)
    
    # 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def url_extract(DataFrame, channel):
    '''DataFrame.description에서 기사 본문 url 추출'''
    
    copy = DataFrame.copy()
    
    url_pattern = {'mbc':r'\bhttps://imnews.imbc.com[/_\w]+.html\b',
                   'sbs':r'(https://news.sbs.co.kr/y/\?id=\w+)',
                   'jtbc':r'기사 전문 https://bit.ly/[\w]+'}
    jtbc_pattern = r'https://bit.ly/[\w]+'
    
    url_list = []
    for element in copy.description:
        temp = re.findall(url_pattern[channel], str(element))
        if temp:
            url = temp[0]
        else:
            url = None
            
        url_list.append(url)
        
    if channel=='jtbc':
        jtbc_url_list = []
        for element in url_list:
            if element:
                url = re.findall(r'https://bit.ly/[\w]+', element)[0]
            else:
                url = None
                
            jtbc_url_list.append(url)
        url_list = jtbc_url_list
    
    copy['article_url'] = url_list
    copy.dropna(axis=0, inplace=True)
    copy.reset_index(drop=True, inplace=True)
    
    return copy


# In[ ]:


def get_article_body(article_url, channel):
    
    selector = {'mbc':'div.news_txt',
                'sbs':'div.main_text > div',
                'jtbc':'div.article_content'}
    req = urllib.request.Request(article_url)
    
    with urllib.request.urlopen(req) as response:
        the_page = response.read()

    try:
        source = BeautifulSoup(the_page, 'html.parser')
        article_text = source.select_one(selector[channel]).text
    except:
        article_text = None
    
    return article_text


# In[ ]:


def article_cleaning(DataFrame, cleaning_function, channel):
    
    copy = DataFrame.copy()
    
    copy.dropna(axis=0, inplace=True)
    copy.reset_index(drop=True, inplace=True)
    
    cleaned_description = [cleaning_function(get_article_body(element, channel)) for element in copy['article_url']]
    copy['cleaned_description'] = cleaned_description

    copy.dropna(axis=0, inplace=True)
    copy.reset_index(drop=True, inplace=True)
    
    copy = copy.loc[copy['cleaned_description'].str.len() > 250]
    copy.reset_index(drop=True, inplace=True)
    
    return copy


# In[ ]:


def mbc_article_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'\r|\n', '', text)
    text = re.sub(r'<.+?>', '', text)
    text = re.sub(r'◀.+?▶', '', text)
    text = re.sub(r'\/', '', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r'\u200b', '', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
    text = text.split('▷')[0]
    
    # [], ()로 쌓여있는 문자열 제거
    text = re.sub(r'(\(.+\))', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'”|“|‘|’', '', text)
    text = re.sub(r'\={2,}', ' ', text)
    text = re.sub(r'‥', ' ', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def sbs_article_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'\r|\n', '', text)
    text = re.sub(r'\&.+?\&.+?;', '', text)
    text = re.sub(r'<.+?>', '', text)
    text = re.sub(r'◀.+?▶', '', text)
    text = re.sub(r'\/', '', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r'\u200b', '', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
#     text = text.split('▷')[0]
    
    # [], ()로 쌓여있는 문자열 제거
#     text = re.sub(r'(\[.+\])', '', text)
    text = re.sub(r'(\(.+\))', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'”|“|‘|’', '', text)
    text = re.sub(r'\={2,}', ' ', text)
    text = re.sub(r'‥', ' ', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# In[ ]:


def jtbc_article_cleaning(text):
    text = str(text)
    # 정규표현식으로 제거
    text = re.sub(r'\r|\n', '', text)
    text = re.sub(r'\&.+?\&.+?;', '', text)
    text = re.sub(r'<.+?>', '', text)
    text = re.sub(r'◀.+?▶', '', text)
    text = re.sub(r'\/', '', text)
    text = re.sub(r"\'|\"", ' ', text)
    text = re.sub(r'\u200b', '', text)
    text = re.sub(r'(Q\.)', '', text)
    text = re.sub(r'\[앵커\]|\[기자\]', '', text)
    text = re.sub(r"(美)", '미국', text)
    text = re.sub(r"(佛)", '프랑스', text)
    text = re.sub(r"(UAE)", '아랍에미리트', text)
    text = re.sub(r"(中)", '중국', text)
    text = re.sub(r"(日)", '일본', text)
    text = re.sub(r"(韓)", '한국', text)
    text = re.sub(r"(北)", '북한', text)
    text = re.sub(r"(■)", '', text)
    text = re.sub(r"(▲)", '', text)
    text = re.sub(r"(靑)", '청와대', text)
    text = re.sub(r"(與)", '여당', text)
    text = re.sub(r"(野)", '야당', text)
    text = re.sub(r"(新)", '신규', text)
    text = re.sub(r"(外)", '외', text)
    text = re.sub(r"(英)", '영국', text)
    text = re.sub(r'인용보도 시 프로그램명 (.+) 을 밝혀주시기 바랍니다\.', '', text)
    text = re.sub(r'저작권은 JTBC에 있습니다\.', '', text)
    text = re.sub(r"방송 \: JTBC 아침\&", '', text)
    text = re.sub(r"방송 \: JTBC 뉴스룸", '', text)
    text = re.sub(r"진행 \: \w{1,}", '', text)
    
    # 단위
    text = re.sub(r'(㎥)', '세제곱미터', text)
    text = re.sub(r'(km)', '킬로미터', text)
    text = re.sub(r'(㎞)', '킬로미터', text)
    text = re.sub(r'(mm)', '밀리미터', text)
    text = re.sub(r'(㎜)', '밀리미터', text)
    text = re.sub(r'(ｍ)|(m)', '미터', text)
    text = re.sub(r'(%)', '퍼센트', text)
    text = re.sub(r'(％)', '퍼센트', text)
    text = re.sub(r'(㎿)', '메가와트', text)
    text = re.sub(r'(㏊)', '헥타르', text)
    text = re.sub(r'(↓)', ' 감소', text)
    text = re.sub(r'(↑)', ' 상승', text)
    
    # #, ▣, ▶ 뒤에 문자열은 다 제거
    text = text.split('※')[0].split('☎')[0]
    
    # [], ()로 쌓여있는 문자열 제거
#     text = re.sub(r'(\[.+\])', '', text)
#      text = re.sub(r'(\(.+\))', '', text)
    
    # 끝 문자가 .이 될때까지 삭제
    try:
        while text[-1] != '.':
            text = text[:-1]
    except:
        pass
    
    # 띄어쓰기 중복으로 되어 있는 부분 정리
    text = re.sub(r'”|“|‘|’', '', text)
    text = re.sub(r'\={2,}', ' ', text)
    text = re.sub(r'‥', ' ', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'·', ', ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

