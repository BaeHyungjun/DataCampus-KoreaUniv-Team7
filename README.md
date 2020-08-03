# YouTube 뉴스 컨텐츠 자동요약 서비스
by. 데이터청년캠퍼스 고려대학교 7조
- 고은경(ek-koh)
- 권지혜(popo97kr)
- 강성권(SungKweon)
- 배형준(BaeHyungjun)

data link : https://drive.google.com/drive/u/0/folders/1EXBU7Cwbb7DhtwldgVqwRTT6IYf9k_Mu

## 프로젝트 설명
`Naver 뉴스, Daum 뉴스`의 게시일자, 제목, 기사본문, 요약문을 크롤링 및 학습하여 `YouTube 뉴스 컨텐츠`를 자동으로 요약하는 서비스를 구현합니다.

## 활용 데이터 수집방안
||Naver|Daum|YouTube|
|:---:|:---:|:---:|:---:|
|수집정보|게시일자 / 제목 / 기사본문 / 요약문|게시일자 / 제목 / 기사본문 / 요약문|영상제목 / 영상 자동생성자막 / 동영상정보 / 댓글|
|수집방안|Beautifulsoup|Beautifulsoup|Beautifulsoup, Selenium|
|수집건수|100,000건|100,000건|1,000건|
|기타|날짜별, 카테고리별 상위 랭킹 뉴스|날짜별, 카테고리별 상위 랭킹 뉴스|YTN, JTBC, SBS, KBS, MBC, 경향신문, 중앙일보, 한겨례...|

## 분석 FLOW
![image](https://user-images.githubusercontent.com/58713684/89136084-d7af5e00-d56c-11ea-9a15-3b4c99c72e7e.png)
  
## 활용 모델
`Attention이 적용된 sequence to sequence 모델`을 사용합니다. 해당 모델은 단어들에 가중치를 주며 학습되는 encoder와 decoder로 구성되어 있으며 이와 같은 구조는 text summarization에 유용하여 가장 자주 쓰이는 모델로 알려져 있습니다.  
![image](https://user-images.githubusercontent.com/58713684/89136169-4987a780-d56d-11ea-9f4c-7dd2687327fe.png)

## 어플리케이션 예상 구현 방안
뉴스 채널에서 업로드되는 영상들을 실시간으로 수집하여, 해당 영상에 미리 학습된 모델을 적용합니다. 영상 옆에 뉴스 영상의 **핵심 키워드**가 표시되며, 영상을 클릭하면 원본 영상이 있는 유튜브 페이지로 이동하고, 키워드를 클릭하면 해당 키워드가 나타난 구간으로 바로 이동합니다.  

더불어 **댓글 요약**을 제공할 예정입니다. 이모티콘 등 구어체의 특수성을 반영해 유튜브 댓글을 두세줄로 요약하여 화면에 표시합니다.

![image](https://user-images.githubusercontent.com/58713684/89136517-1b0acc00-d56f-11ea-9115-2fb31f3dbeb8.png)
  

## 기대효과
|서비스 이용자|언론사|
|:---|:---|
|정보의 홍수 속에서 양질의 정보 선택 용이|정확한 정보전달을 통해 언론 신뢰도 향상|
|시간 단축을 통한 효율적 컨텐츠 소비 가능|뉴스컨텐츠 제공 형식의 다양화로 유튜브 시청자들의 접근성 향상|




