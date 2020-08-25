# EDA 정리를 위한 문서

## Summary 문장의 위치  
Summary의 문장들은 기사 본문의 어느 부분에 가장 많이 위치해 있을까요?

![image](https://user-images.githubusercontent.com/58713684/90093342-558e1900-dd66-11ea-9be9-4887bfc36fd1.png)
  
    
```py
from collections import Counter
c = Counter(summary_loc_list)
c.most_common(20)
```    

|위치(%)|count|
|:---|---:|
|6|14200|
|8|13765|
|5|13257|
|7|12399|
|4|12314|
|12|11222|
|100|9905|
|11|9879|
|3|9694|
|10|9501|
|50|8918|
|9|8852|
|14|8400|
|17|8025|
|33|7763|
|25|7359|
|20|7302|
|18|5478|
|29|5329|
|67|5067|
 

- 현재까지는 daum 뉴스 데이터만 가지고 수행한 결과입니다.
- Summary에 포함된 문장이 기사 본문에서 어떤 위치에 있는지를 인덱스로 나타낸 후, 각 기사의 문장 개수가 다양한 점을 고려하여 비율로 나타내 일반화하였습니다.
- 대부분 10% 이하의 위치에서 나타났으므로, 첫번째 문장과 첫번째 문단이 중요함을 추측해볼 수 있습니다.
- 이 외에도 마지막 문장(100%), 중간 지점의 문장(50%), 1/3, 1/4, 1/5 지점의 문장이 summary로 많이 추출되었던 것을 확인할 수 있었습니다.

## 불용어 확인  

![image](https://user-images.githubusercontent.com/58713684/90409410-13593480-e0e4-11ea-9f41-86d19241207c.png)
  
가장 많이 등장한 70개의 단어를 뽑아보았을 때, 그림과 같이 앞의 64개 단어들(~, 그)은 분석에서 중요하지 않은 불용어라고 판단하여 분석에서 제외하였습니다.  

## 연도별 WordCloud  

![image](https://user-images.githubusercontent.com/58713684/90980380-f1edc200-e595-11ea-9188-059fa61e7442.png)  

![image](https://user-images.githubusercontent.com/58713684/90980394-016d0b00-e596-11ea-9d4f-f52bea58e9f8.png)
  
![image](https://user-images.githubusercontent.com/58713684/90980403-0f229080-e596-11ea-9073-20940df34be1.png)
  
![image](https://user-images.githubusercontent.com/58713684/90980406-1c3f7f80-e596-11ea-9bb6-65d639d3f0e9.png)
  
- 2017 ~ 2019년에 비해 2020년에는 코로나19와 관련된 단어들이 많이 등장하게 되었음을 확인할 수 있습니다.  





