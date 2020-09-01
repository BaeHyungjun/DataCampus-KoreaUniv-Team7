# YouTube Summary : YouTube 뉴스 컨텐츠 자동요약 서비스
by. 데이터청년캠퍼스 고려대학교 7조
- 고은경(ek-koh)
- 권지혜(popo97kr)
- 배형준(BaeHyungjun)

## 프로젝트 설명
`Naver 뉴스, Daum 뉴스`의 게시일자, 제목, 기사본문, 요약문을 크롤링 및 학습하여 `YouTube 뉴스 컨텐츠`를 자동으로 요약하는 서비스를 구현합니다.  

## 구조
1. **Crawling** : Naver 뉴스와 Daum 뉴스, YouTube 뉴스에서 각각 크롤링 및 스크래핑하여 데이터를 수집한 코드입니다.
2. **Preprocessing** : Naver, Daum, YouTube 데이터에 대해 Data Cleaning, Tokenizing, Normalizing, Stemming, Integer Encoding 등의 전처리를 수행한 코드입니다.
3. **CommentSentimentAnalysis** : YouTube 뉴스영상의 댓글을 활용해 감성분석을 진행한 코드입니다.
4. **Modeling** : 학습을 위한 모델 관련 코드입니다.
5. **Flask** : PC/모바일 웹 및 어플리케이션 구현을 위한 코드입니다.  

> **전체 과정 정리** : 위의 1 ~ 5 항목에 존재하는 소스코드 중 실제 최종 결과물에 반영된 소스코드만을 작업순서에 따라 재배열한 폴더입니다. 즉, 내용은 1 ~ 5 항목에 나타난 것과 같으니 전체 진행과정을 확인하기 위한 참고용으로 사용하시기 바랍니다.  

## 데이터 & 학습모델  
구글 드라이브 link: https://drive.google.com/drive/u/0/folders/1EXBU7Cwbb7DhtwldgVqwRTT6IYf9k_Mu  

- [데이터](https://drive.google.com/drive/u/0/folders/10IFZEeVduhyJR4LZlH9iHobNBvRHfyAg)
- [학습모델](https://drive.google.com/drive/u/0/folders/1YC38uwdjvp77PNPvw12OkeSMBITJPW__)

## 배경 및 필요성  
최근 TV보다는 스마트폰으로, 그리고 그 중에서도 SNS를 통해 뉴스를 소비하는 비율이 점점 높아지고 있습니다. 한국언론진흥재단에서 조사한 바에 따르면, 2019년 1월 기준 주요 22개 언론사의 SNS 구독자 수 총합은 약 1600만 명이라고 합니다. 페이스북, 트위터, 인스타그램, 유튜브, 네이버, 다음 등 뉴스를 제공하는 플랫폼은 다양하지만 저희 팀은 그 중에서 유튜브를 주목하였습니다.  
  
여러 플랫폼 중 유튜브를 선택한 이유는 가장 눈에 띄는 성장세를 보이고 있기 때문입니다. 2018년 2월 와이즈앱에서 발표한 통계에 따르면, 유튜브는 2016년부터 2018년 사이에 사용시간이 3배 이상 증가하여 타 매체(카카오, 네이버, 페이스북, 다음)보다 사용량이 월등히 높은 수준에 있습니다. 추세를 보면 2020년엔 더 많이 소비되고 있을 것이라고 추정해볼 수 있습니다.  
  
이에 따라 뉴스기사 또한 타 매체보다 YouTube를 통해 접하는 사용자가 급증하고 있는데, 실제로 YouTube 인기동영상의 많은 부분이 뉴스 컨텐츠로 구성되어 있기도 합니다. 또한 영국 로이터저널리즘연구소 [디지털 뉴스 리포트 2020](http://www.digitalnewsreport.org/)에 따르면, SNS로 뉴스를 접한다는 국내 응답자 비율은 44%(복수 응답)로 2019년 26%보다 큰 폭으로 증가했고 SNS를 통한 뉴스 이용 매체로 YouTube를 꼽은 응답자는 45%였습니다.  
  
하지만, 이렇게 유튜브 뉴스 콘텐츠에 대한 수요가 많더라도, 바쁜 현대인들이 끊임 없이 생산되는 콘텐츠를 편향되지 않게 모두 본다는 것은 불가능에 가까울 것입니다. 따라서 콘텐츠를 단순히 많이 소비하는 것보다는 핵심만 골라서 소비하는 전략이 필요합니다. 저희는 여기서 저희의 유튜브 뉴스 요약 서비스가 필요한 이유를 찾았습니다. 밀리의 서재, 유튜브 영화 서머리, AI 가 선정한 스포츠 경기 하이라이트 등 서머리(summary) 산업이 부상하고 있는 현 시점에서, 저희의 서비스 또한 타임푸어(Time Poor)족의 서머리 콘텐츠 소비 욕구를 충족시켜줄 수 있을 것입니다.  


## 활용 데이터 수집
|     |Naver|Daum|YouTube|
|:---:|:---:|:---:|:---:|
|수집정보|게시일자 / 제목 / 기사본문 / 요약문|게시일자 / 제목 / 기사본문 / 요약문|영상제목 / 영상 스크립트 / 댓글|
|수집방안|Beautifulsoup|Beautifulsoup|Pytube & YouTube API|
|수집건수|약 112,466건|약 109,419건|실시간|
|활용방안|Training / Validation|Training / Validation|Test|
|기타|최근 약 2년간의 날짜별, 카테고리별 상위 랭킹 뉴스|최근 약 3년간의 날짜별, 카테고리별 상위 랭킹 뉴스|YTN, SBS, KBS, MBC, JTBC, MBN, 채널A, 연합뉴스|  

## 분석 / 개발 환경  
![image](https://user-images.githubusercontent.com/58713684/91732327-0e67ab00-ebe3-11ea-8160-fbfe9a782811.png)
  
- 크롤링에 사용한 라이브러리는 `Requests`, `BeautifulSoup`, `pytube`, `YoutubeAPI`이며 수집한 텍스트 데이터를 전처리하는데 `KoNLPy`와 `NLTK`를 사용하였습니다.  
- 데이터 핸들링에는 `pandas`, `sqlite`를 사용하였고, `matplotlib`, `wordcloud`를 이용하여 시각화하였으며 요약 모델에는 `tensorflow`와 `Gensim`을 이용하였습니다.  
- 서비스 개발은 `pycharm`에서 `flask`와 `azure mysql`을 연동하여 이용했고, 앱 제작을 위해 `Swing2App`을 사용했습니다.


## 시스템 흐름도
![image](https://user-images.githubusercontent.com/58713684/91732396-263f2f00-ebe3-11ea-915f-dbb6cbd91140.png)
    
- train data로 네이버와 다음 뉴스에서 기사본문을 x값으로, 요약문을 y값으로 하여 tokenizing을 한 후, koNLPy를 사용해 모델 학습을 위한 전처리를 진행합니다. 
- 키워드 추출 모델을 학습시켜 기사를 대표하는 키워드를 뽑았고, textrank 알고리즘을 사용하여 문서를 요약하는 gensim summarizer를 이용하여 요약문을 추출하였습니다.


## EDA
EDA 결과는 [EDA.md](https://github.com/BaeHyungjun/DataCampus-KoreaUniv-Team7/blob/master/preprocessing/EDA.md)에 정리합니다.  

- 월별 groupby해서 워드클라우드
- Summary에서 나온 문장들이 본문에서는 어디에 분포하는지 시각화
- Zipf's law: 불용어 처리를 위해 단어 빈도수 barplot (정렬)

  
## 활용 모델
`Attention이 적용된 sequence to sequence 모델`을 사용합니다. 해당 모델은 단어들에 가중치를 주며 학습되는 encoder와 decoder로 구성되어 있으며 이와 같은 구조는 text summarization에 유용하여 가장 자주 쓰이는 모델로 알려져 있습니다.  
  
**Seq2Seq with Attention**  
![image](https://user-images.githubusercontent.com/58713684/89136169-4987a780-d56d-11ea-9f4c-7dd2687327fe.png)

## 웹 / 어플리케이션 구현  
기존 유튜브와 같이 썸네일과 제목을 제공하고 하단에 영상 키워드와 영상 요약, 댓글 요약과 댓글 반응 감성분석 내용을 제공합니다. 영상 시청 전 요약문을 미리 확인하여 영상을 시청하지 않고 영상 내용에 대한 정보를 빠르게 습득하여 효율적인 뉴스 콘텐츠 소비가 가능하도록 만들었습니다.  
그럼에도 영상을 보고 싶다면 영상 썸네일을 클릭하여 원본 영상이 있는 유튜브로 이동하여 영상을 시청할 수 있게 만들었습니다.

![image](https://user-images.githubusercontent.com/58713684/91732204-e37d5700-ebe2-11ea-8824-5b7e0ddef4be.png)  

영상 요약뿐만 아니라 키워드 랭킹 정보와 워드 클라우드를 활용하여 일간리포트를 제공하고 있습니다. 이는 영상의 요약문조차 확인할 시간이 없는 소비자들에게 유용한 서비스가 될 수 있을 것입니다.  
또한 원하는 언론사의 영상만 모아서 볼 수 있는 페이지도 구현하였습니다.

![image](https://user-images.githubusercontent.com/58713684/91732493-440c9400-ebe3-11ea-91af-5c2562905adf.png)  

본 서비스에서는 현대인들이 보다 간편하게 컨텐츠를 소비할 수 있도록 모바일 웹 / 앱 구현에 초점을 맞추었지만, PC 웹 페이지 또한 구현하였습니다.  

![image](https://user-images.githubusercontent.com/58713684/91733077-11af6680-ebe4-11ea-9d52-d4cbb2eb4bd9.png)
  
  
## 기존 서비스와의 차별성
- `네이버, 다음의 요약 서비스` : 네이버뉴스, 다음뉴스는 텍스트가 주된 기반이지만, 저희의 유튜브 뉴스컨텐츠 자동요약 서비스는 텍스트요약과 영상을 함께 제공한다는 점에서 매체의 다양성이라는 강점이 있습니다.
- `기존 YouTube 내 요약정보 제공 영상` : 기존의 요약 영상들은 분석 및 영상편집에 시간이 소요되는 반면, 저희의 유튜브 뉴스컨텐츠 자동요약 서비스는 ML/DL을 적용하므로 실시간으로 업로드되는 영상들에 대해 빠른 요약 결과를 제공할 수 있다는 강점이 있습니다.

## 기대효과
|서비스 이용자|언론사|사회|
|:---|:---|:---|
|정보의 홍수 속에서 양질의 정보 선택 용이|시청자들의 선택의 폭이 증가하여 경쟁력 확보를 위한 정확한 정보전달 노력으로 언론 신뢰도 향상|유튜브 알고리즘으로 인한 확증편향을 방지하여 국민 지식수준 향상|
|시간 단축을 통한 효율적 컨텐츠 소비 가능|기존에 긴 기사 / 영상은 보지 않던 신규 시청자 유입 창출|타임푸어(Time Poor)족의 뉴스 소비를 촉진시킴으로써 정보격차 해소에 일조|


