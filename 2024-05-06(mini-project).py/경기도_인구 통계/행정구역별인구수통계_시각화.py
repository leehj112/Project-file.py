# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:01:19 2024

@author: dlgur
"""

import pandas as pd

df_merge = pd.read_csv('./행정구역별_인구수_2019-202404.csv', index_col= 'Unnamed: 0')

#%%
import matplotlib.pyplot as plt
# 한글 폰트 설정
from matplotlib import font_manager, rc
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font_name)

###############################################################################
# 연도별 '경기도' 전체/ 65세이상 인구수 변화
###############################################################################
op_area = df_merge['행정구역']=='경기도'
op_col = list(filter(lambda x: '전체' in x, df_merge.columns))
op_df = df_merge.loc[op_area, op_col]


gg_people = pd.DataFrame({'연도' : [2019, 2020, 2021, 2022, 2023, 2024],
                          '전체' : [op_df.iloc[0,0], op_df.iloc[0,2], op_df.iloc[0,4], op_df.iloc[0,6], op_df.iloc[0,8], op_df.iloc[0,10]],
                          '65세이상' : [op_df.iloc[0,1], op_df.iloc[0,3], op_df.iloc[0,5], op_df.iloc[0,7], op_df.iloc[0,9], op_df.iloc[0,11]]
                          })
gg_people['65세이상비율'] = (gg_people['65세이상'] / gg_people['전체']) * 100 


#%% 시각화
# 연도별 인구수
plt.plot(gg_people['연도'], gg_people[['전체', '65세이상']], linestyle='-')
plt.title('연도별 인구수')
plt.xlabel('연도')
plt.ylabel('전체인구수')
plt.grid(True)
plt.show()

# 노인 구분에 따른 인구수 비율
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
labels = ['일반', '노인']
tot_driver = gg_people.iloc[5, 1] # 2024년 전체
tot_elderly_driver = gg_people.iloc[5, 2] # 2024년 65세이상
tot_regular_driver = tot_driver - tot_elderly_driver

sizes = [tot_regular_driver, tot_elderly_driver]
colors = ['lightgreen', 'lightsalmon']
explode = (0.1, 0)  # 강조를 위한 explode
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('2024년 4월 인구수 구분 비율(%)')