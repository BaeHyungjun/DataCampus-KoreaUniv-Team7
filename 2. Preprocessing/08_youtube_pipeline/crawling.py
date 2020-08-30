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


def transform_duration(time):
    '''
    유튜브 동영상 duration이 지저분해서 깔끔하게 바꾸는 함수
    
    time : video duration ex. 'PT3H14M16S'
    '''
    time_list = re.split(r'H|M|S', re.sub(r'PT', '', time))
    
    if len(time_list) == 4:
        time_as_second = 3600*int(time_list[0]) + 60*int(time_list[1]) + int(time_list[2])
    elif len(time_list) == 3:
        time_as_second = 60*int(time_list[0]) + int(time_list[1])
    elif len(time_list) == 2:
        time_as_second = int(time_list[0])
    
    return time_as_second


# In[ ]:


def get_channel_video_id(channel_id, api_key, start_time, end_time):
    '''
    유튜버의 영상 중 해당 기간 내에 업로드 된 영상들을 가져오는 함수
    
    channel_id : 유튜버의 채널 id
    
    api_key : YoutubeAPI에서 발급받은 api key
    
    start_time : 영상을 가져올 시작 시간 ex. '2020-08-01 00:00:00'
    
    end_time : 영상을 가져올 종료 시간 ex. '2020-08-04 00:00:00'
    '''
    # youtube resource에 접근하기 위한 객체 생성
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # 해당 채널에서 '업로드 된 동영상' 재생 목록의 id 값을 가져오기
    channel_res = youtube.channels().list(id=channel_id,
                                          part='contentDetails').execute()
    playlist_id = channel_res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # 자료 저장과 종료 조건 체크를 위한 객체 생성
    videos = []
    video_info_list = []
    base_url = 'https://www.youtube.com/watch?v='
    next_page_token = None
    
    # 데이터 수집
    while True:
        # 재생 목록에 대해 영상 list를 추출, 가장 최신의 동영상부터 순차적으로 가져옴
        video_res = youtube.playlistItems().list(playlistId=playlist_id,
                                                 part='contentDetails',
                                                 maxResults=50, 
                                                 pageToken=next_page_token).execute()
        # 저장 조건 체크 및 자료 저장
        for item in video_res['items']:
            try:
                temp_date = re.sub('Z', '',re.sub('T', ' ', item['contentDetails']['videoPublishedAt']))

                if start_time <= temp_date <= end_time:
                    videos.append(item)

                    published_time = temp_date
                    video_id = item['contentDetails']['videoId']
                    video_url = base_url + item['contentDetails']['videoId']

                    # 영상 길이가 10분 이하일때 저장 : 너무 길면 pytube.YouTube로 가져오는데 너무 오래 걸림
                    res_content = youtube.videos().list(id=video_id, part='contentDetails').execute()
                    duration = transform_duration(res_content['items'][0]['contentDetails']['duration'])

                    if duration <= 600:
                        video_info_list.append([published_time, video_id, video_url])
            
            except:
                continue
        
        # 종료 조건을 위한 값 생성 및 조건 체크
        next_page_token = video_res.get('nextPageToken')
        criteria_date = re.sub('Z', '',
                               re.sub('T', ' ',
                                      video_res['items'][0]['contentDetails']['videoPublishedAt']))
        
        # 종료 조건 1 : 새로 수집 된 영상의 업로드 시간이 시작 시간보다 앞설 때 종료
        if criteria_date < start_time:
            break
            
        # 종료 조건 2 : 더 이상 수집할 데이터가 없을 때 종료    
        if next_page_token is None:
            break
    
    video_info_df = pd.DataFrame(video_info_list, columns=['published_time', 'video_id', 'video_url'])
    video_info_df.sort_values(by='published_time', inplace=True, ignore_index=True)
    
    return video_info_df


# In[ ]:


def get_video_info(case):
    '''
    pytube를 이용하여 동영상의 저자, 제목, 링크, 영상 길이(초), 평점, 썸네일 링크, 조회수, 영상 설명, 자동 생성 자막을 가져오는 함수
    영상의 description에 뉴스 영상 스크립트가 있으면 이 함수를 사용
    사용 가능 언론사 : YTN, KBS, 연합뉴스, 채널A, MBN
    
    case : get_channel_video_id의 return DataFrame 중 하나의 case
    '''
    published_time = case['published_time']
    video_id = case['video_id']
    video_url = case['video_url']
    
    try:
        # 영상 가져오기
        source = YouTube(video_url)
        
        # 영상 정보 추출
        crawling_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author = source.author
        title = source.title
        length = source.length
        rating= source.rating
        views = source.views
        thumbnail_url= source.thumbnail_url
        
        try:
            captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        except:
            captions = None
        
        description = source.description
        
        video_info = [published_time, video_id, video_url,
                      crawling_time, author, title, length, rating, views, thumbnail_url, captions, description]
    
    # 영상 정보를 가져오는데 실패한 경우
    except: 
        video_info = [published_time, video_id, video_url,
                      None, None, None, None, None, None, None, None, None]
    
    return video_info


# In[ ]:


def get_video_infos(video_info_df):
    '''
    복수의 video_url에 대해 영상 정보 가져오기
    사용 가능 언론사 : YTN, KBS, 연합뉴스, 채널A, MBN
    
    video_info_df : get_channel_video_id의 return DataFrame
    '''
    video_info_list = []
    row_number = len(video_info_df)
    start = time.time()

    for index in range(row_number):
        case = video_info_df.iloc[index]
        video_info = get_video_info(case)
        video_info_list.append(video_info)
        
        # 진행상황 출력
        if index % 100 == 0:
            during = time.time() - start
            during_min = int(during // 60)
            during_second = round(during % 60)
            
            print('진행 상황 : {} / {} ({}%), {}분 {}초동안 돌아가는 중'                  .format(index, row_number, round(100 * index / row_number), during_min, during_second))
    
    # DataFrame으로 저장
    video_info_df = pd.DataFrame(video_info_list,
                                 columns=['published_time', 'video_id', 'video_url',
                                          'crawling_time', 'author', 'title', 'length', 'rating', 'views',
                                          'thumbnail_url', 'captions', 'description'])
    
    return video_info_df


# In[ ]:


def get_comments(video_id, youtube_build, max_results=20):
    '''동영상의 comment 관련도 높은 순으로 가져오기
    
    video_id : 동영상의 id
    
    youtube_build : youtubeapi의 build 객체
    
    max_results : 최대 결과 개수, 최소 1개 ~ 최대 100개, default : 20
    '''
    try:
        comment_info = youtube_build.commentThreads().list(videoId=video_id,
                                                     part='snippet',
                                                     maxResults=max_results,
                                                     order='relevance').execute()

        comment_list = [item['snippet']['topLevelComment']['snippet']['textOriginal']
                        for item in comment_info['items']]
    except:
        comment_list = None
    
    return comment_list


# In[ ]:


def add_comments_df(youtube_df, api_key, results=20):
    '''youtube_crawling했던 DataFrame에 comments 열 추가하기
    
    youtube_df : 크롤링했던 DataFrame
    
    api_key : youtube api에서 발급받은 key
    
    results : 최대 결과 개수, 최소 1개 ~ 최대 100개, default : 20
    '''
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    video_id_list = youtube_df['video_id']
    
    comments_list = [[get_comments(video_id, youtube, max_results=results)]
                    for video_id in video_id_list]

    comments_df = pd.DataFrame(comments_list, columns=['comments'])
    
    return pd.concat([youtube_df, comments_df], axis=1)

