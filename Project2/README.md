# 16101894 안재홍 Project2 : US Presidential Election Analysis

* **Note 1**: 해당 프로젝트는 https://gist.github.com/conorosully를 참고하였음을 알려드립니다.
* **Note 2**: 해당 프로젝트의 모든 데이터는 *Harvard Dataverse*, *MIT Election lab* 그리고 *US Census Bureau*에서 가져왔습니다. 



1. 밑의 그림은 50개주은 선거결과를 지도에 mapping 한 것 입니다. 기존 source에 코드를 수정/첨가 하여, 각 주별 득표 비율에 따라 Democrat과 Republican의 색을 파란색 계열과 빨간색 계열로 표시함에 어느 주가 어떤 성향을 보이는지 보여줍니다. 

<img src="./screenshot1.png" alt="screenshot1" style="zoom:33%;" />



2. 아래 9개 사진은 미국의 각 state을 9개의 구역으로 나누고, 인접 주들과 *Correlation*을 나타낸 것이다. 
   * 같은 구역 내여도 영토의 면적이 넓은 지역 (Ex. Colorado와 Wyoming)과 같은 주들은 상호 연관성이 떨어지는 경우가 있다.
   * 인접 주들 중 경제가 같이 돌아가는 지역들은 (Ex. New York과 New Jersey 혹은 Virginia, Maryland & D.C.)와 같은 주들은 상호 연관성이 높다.
   *  인구 구성이 비슷한 주들은 (Ex. South Dakota와 North Dakota) 상호 연관성이 높다고 볼 수 있다.

위 3개와 같은 특성들을 밑 Table에서 찾아볼 수 있다. 

 <img src="./screenshot2.png" alt="screenshot2" style="zoom:50%;" /><img src="./screenshot3.png" alt="screenshot3" style="zoom:50%;" />

<img src="./screenshot4.png" alt="screenshot4" style="zoom:50%;" /><img src="./screenshot5.png" alt="screenshot5" style="zoom:50%;" /><img src="./screenshot6.png" alt="screenshot6" style="zoom:50%;" /><img src="./screenshot7.png" alt="screenshot7" style="zoom:50%;" />

<img src="./screenshot8.png" alt="screenshot8" style="zoom:50%;" />  <img src="./screenshot9.png" alt="screenshot9" style="zoom:50%;" />

<img src="./screenshot10.png" alt="screenshot10" style="zoom:50%;" />

3. 위 사진들은 선거 데이터가 1976년부터 이므로 현 상황과 다를 수도 있다. 따라서, 가장 최근 선거중 4개를 선택하여, 각 주별 평균 지지율을 나타내보았다.

   (밑 자료는 Democrat기준으로 percentage 측정이 되었으므로 Republican 기준으로 보려면, abs(100-avg))를 수행하여야한다.)

   <img src="./screenshot11.png" alt="screenshot11" style="zoom:50%;" /><img src="./screenshot12.png" alt="screenshot12" style="zoom:50%;" />

4.  최근 4개의 선거로 2번에 수행하였던 *Correlation*을 다시 구해보았다.

   * 위 자료와 비교해 보았을때, [*Bible Belt*](https://en.wikipedia.org/wiki/Bible_Belt) 와 [*Rust Belt*](https://en.wikipedia.org/wiki/Rust_Belt) 에서의 변화를 볼 수 있다.
   * Bible Belt: 대표적으로 Georgia 주의 변화를 볼 수 있다. 위의 전체 선거에 대한 상관관계에서는 North Carolina와 South Carolina와의 상관관계가 높았지만, 최근 4개에선 상관관계가 줄어들었다.
   * Rust Belt: Illinois주를 제외한 나머지 주들간의 상관관계가 높아짐을 볼 수 있다. 

   <img src="./screenshot14.png" alt="screenshot14" style="zoom:50%;" /><img src="./screenshot15.png" alt="screenshot15" style="zoom:50%;" />

   <img src="./screenshot16.png" alt="screenshot16" style="zoom:50%;" /><img src="./screenshot17.png" alt="screenshot17" style="zoom:50%;" />

   <img src="./screenshot18.png" alt="screenshot18" style="zoom:50%;" /><img src="./screenshot19.png" alt="screenshot19" style="zoom:50%;" />

   <img src="./screenshot20.png" alt="screenshot20" style="zoom:50%;" /><img src="./screenshot21.png" alt="screenshot21" style="zoom:50%;" />

   <img src="./screenshot22.png" alt="screenshot22" style="zoom:50%;" />

   5. 아래는 1번을 응용하여, 3243개의 카운티 별로 mapping 한 것이다. 

      (2020년 대선은 우편, 현장 등 투표 종류가 다양해져, 실제 득표와 오차가 있는 카운티들이 존재합니다.)

   <img src="./screenshot23.png" alt="screenshot23" style="zoom:50%;" />



* 1976년부터 2020년 선거 데이터를 이용하여, 여러가지 시각화를 진행하였다.
* 지도의 형태를 보여주는 shapefile과 선거 데이터를 가지고 있는 결과 파일의 지명 표기법 등이 달라 matching 하기가 상당히 번거로운 작업이였다. 
* *Correlation*을 이용하여, 각 주마다의 상관관계를 알고, folium으로 지도 시각화를 통하여, 한눈에 선거 결과를 볼 수 있었다. 
* 각 DataFrame을 변형하여 새로운 결과를 나타낼 수 있었다.