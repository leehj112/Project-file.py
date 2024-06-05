# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:16:40 2024

@author: dlgur
"""


# 라이브러리 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기 -> 만들어진 df 확인시 앞과 뒤에 불필요한게 있어서 처리해야함
df = pd.read_excel('202404월말_경기도운전면허소지현황.xlsx')


# 데이터 탐색
df.shape # (7327, 9)

# 데이터 확인
# df 확인시 앞 뒤에 불필요한 내용이 있어 정제예정
df.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7327 entries, 0 to 7326
Data columns (total 9 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   운전면허소지자 현황(시군구, 연령, 대장별)  7327 non-null   object
 1   Unnamed: 1                7324 non-null   object
 2   Unnamed: 2                7324 non-null   object
 3   Unnamed: 3                7324 non-null   object
 4   Unnamed: 4                7324 non-null   object
 5   Unnamed: 5                7324 non-null   object
 6   Unnamed: 6                7324 non-null   object
 7   Unnamed: 7                7324 non-null   object
 8   Unnamed: 8                7324 non-null   object
dtypes: object(9)
memory usage: 515.3+ KB
'''

# 데이터 컬럼명부터 재지정
df.rename(columns={'운전면허소지자 현황(시군구, 연령, 대장별)': '집계월', 
                   'Unnamed: 1': '도', 'Unnamed: 2': '시군구', 'Unnamed: 3': '지역별', 
                   'Unnamed: 4': '성별','Unnamed: 5': '나이',
                   'Unnamed: 6': '종합계', 'Unnamed: 7': '1종소계', 'Unnamed: 8': '2종소계'}, inplace=True)

# 불필요한 열 삭제(0,1,2,7326 이상)
df = df.drop([0,1,2]) 
df = df.drop([7326])

# 집계월은 동일하니 인덱스로 설정
df = df.set_index('집계월') 

# 잘 처리 되었나 확인하기
df.head()
df.tail()
df.info()

'''
<class 'pandas.core.frame.DataFrame'>
Index: 7323 entries, 202404말 to 202404말
Data columns (total 8 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   시도      7323 non-null   object
 1   시군구     7323 non-null   object
 2   지역별     7323 non-null   object
 3   성별      7323 non-null   object
 4   나이      7323 non-null   object
 5   종합계      7323 non-null   object
 6   1종소계    7323 non-null   object
 7   2종소계    7323 non-null   object
dtypes: object(8)
memory usage: 514.9+ KB
'''


# 이제 nan 값이 있나 확인부터 하기(True면 nan값이 존재)
df_for_nan = df.isnull().values.any()
print(df_for_nan)  # False 

# 몇개나 있나?
total_nan_values = df.isnull().sum().sum()
print(total_nan_values) # 0

#%%
# 다른 데이터 타입을 가진 컬럼 확인 : include='all'
# object 타입의 컬럼을 top으로 최빈값 확인
df.describe(include='all')
'''
          시도       시군구       지역별    성별    나이    종합계  1종소계  2종소계
count   7323      7323      7323  7323  7323  7323  7323  7323
unique     1        52        52     2    85  3045  2288  1841
top       경기  경기 성남 분당  경기 성남 분당     남    64     1     0     1
freq    7323       167       167  3840    99   318   676   305
''' 

object_columns = df.columns[df.dtypes == 'object']
object_columns 
'''Index(['도', '시군구', '지역별', '성별', '나이', '종합계', '1종소계', '2종소계'], dtype='object')'''


# '나이, 합계, 1종소계, 2종소계'는 데이터가 숫자니 int로 변경하기
# for문 활용하여 다른 컬럼의 값들 확인
for col in object_columns:
    print(col)
    print(df[col].unique(), '\n')
    

# for 문 결과보니 '나이, 합계, 1종소계, 2종소계'는 데이터가 숫자니 int로 변경
df['나이']  = df['나이'].astype('int')
df['종합계']  = df['종합계'].astype('int')
df['1종소계']  = df['1종소계'].astype('int')
df['2종소계']  = df['2종소계'].astype('int')

df.info()

#%%
# 지역 내용 처리하기(도, 시군구, 지역별)
# 원본 자료에 '도, 시군구, 지역별' 값이 비슷함에 확인하기
print(df['도'].equals(df['시군구'])) # False
print(df['시군구'].equals(df['지역별'])) # True

# 값이 같으니 정제하기
# 시군구 값을 'split(' ')'로 쪼개기
df['지역리스트'] = df['시군구'].str.split(' ')

## 시군구 값을 두번째 리스트인 시까지만 남기고 새로운 컬럼 만들기
def region_second_value(df):
    return df[1]

# 상위값 데이터 할당하기
df['시'] = df['지역리스트'].apply(region_second_value) 


# 3번째 리스트 값 처리 하기
def process_region(df):
    gu = []  # 빈 리스트 생성
    for i in range(len(df['지역리스트'])):
        if len(df['지역리스트'][i]) == 3:
            gu.append(df['지역리스트'][i][2])
        else:
            gu.append('기타') # 빈 값은 기타로 처리
    df['구'] = gu  # 새로운 열 '구' 추가 및 할당
    return df

# 함수 호출
ndf = process_region(df)

# 중복되는 '지역별'과 필요없는 '지역리스트' 지우기
ndf = ndf.drop(columns=['지역별'])
ndf = ndf.drop(columns=['지역리스트'])
print(ndf)

# 마지막으로 가독성있게 컬럼 재배치
ndf = ndf[['시군구', '도', '시', '구', '성별', '나이', '1종소계', '2종소계', '종합계']]
print(ndf)