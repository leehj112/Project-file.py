# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:13:34 2024

@author: dlgur
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 시각화하기 위해 폰트 설정
plt.rc('font', family='Malgun Gothic')

# 연령대 확인 및 구분
ndf['나이'].unique()
'''array([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
       33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
       50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
       67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
       84, 85, 86, 87, 88, 89, 90, 91, 92, 95, 99, 93, 94, 96, 97, 98,  0])'''

# 65세 미만이면 일반운전자, 65세 이상이면 노인운전자로 분류

def calc_age_group(age):
    if age < 65:
        return '일반운전자'    
    else:
        return '노인운전자'

ndf['운전자구분'] = ndf['나이'].apply(calc_age_group)
ndf['운전자구분'].unique() # array(['일반운전자', '노인운전자'], dtype=object)



#%%
# 전체 인원
total_driver = ndf['종합계'].sum() # 9417025/전체 인원

# 성별에 따른 합계 및 비율
def calc_tot_and_ratio_by_gender(df, gender):
    gender_df = df[df['성별'] == gender]
    total_sum = gender_df['종합계'].sum()
    ratio_driver = (total_sum / total_driver) * 100
    return total_sum, ratio_driver

tot_male_sum, ratio_male_driver = calc_tot_and_ratio_by_gender(ndf, '남')
tot_female_sum, ratio_female_driver = calc_tot_and_ratio_by_gender(ndf, '여')
print("남성 합계:", tot_male_sum)  # 남성 합계: 5307631
print(f"남성 운전자 비율: {ratio_male_driver:.0f}%") # 남성 운전자 비율: 56%

print("여성 합계:", tot_female_sum) # 여성 합계: 4109394
print(f"여성 운전자 비율: {ratio_female_driver:.0f}%") # 여성 운전자 비율: 44%

#%%
# 운전자 구분에 따른 합계와 비율
def calc_tot_by_driver_type(df, driver_type):
    driver_df = df[df['운전자구분'] == driver_type]
    total_sum = driver_df['종합계'].sum()
    return total_sum

tot_regular_driver_sum = calc_tot_by_driver_type(ndf, '일반운전자') # 합계
tot_elderly_driver_sum = calc_tot_by_driver_type(ndf, '노인운전자')
ratio_regular_driver = (tot_regular_driver_sum / total_driver) * 100 # 비율
ratio_elderly_driver = (tot_elderly_driver_sum / total_driver) * 100

print("일반운전자의 합계:", tot_regular_driver_sum) # 일반운전자의 합계: 8278493
print("노인운전자의 합계:", tot_elderly_driver_sum) # 노인운전자의 합계: 1138532
print(f"일반운전자 비율: {ratio_regular_driver:.0f}%")  # 일반운전자 비율: 88%
print(f"노인운전자 비율: {ratio_elderly_driver:.0f}%")  # 노인운전자 비율: 12%

#%%
# 노인운전자와 성별 매칭

def calc_tot_by_gender_and_driver_type(df, gender, driver_type):
    driver_df = df[(df['운전자구분'] == driver_type) & (df['성별'] == gender)]
    total_sum = driver_df['종합계'].sum()
    return total_sum

tot_elderly_female_sum = calc_tot_by_gender_and_driver_type(ndf, '여', '노인운전자')
tot_elderly_male_sum = calc_tot_by_gender_and_driver_type(ndf, '남', '노인운전자')

print("여성 노인운전자의 합계:", tot_elderly_female_sum) # 여성 노인운전자의 합계: 389575
print("남성 노인운전자의 합계:", tot_elderly_male_sum)  # 남성 노인운전자의 합계: 748957

ratio_elderly_female_driver = (tot_elderly_female_sum / tot_female_sum) * 100
print(f"노인 여성 운전자 비율: {ratio_elderly_female_driver:.0f}%") # 노인 여성 운전자 비율: 9%

ratio_elderly_male_driver = (tot_elderly_male_sum / tot_female_sum) * 100
print(f"노인 남성 운전자 비율: {ratio_elderly_male_driver:.0f}%") # 노인 남성 운전자 비율: 18%


# 일반운전자와 성별 매칭

def calc_tot_and_ratio_by_gender_and_driver_type(df, gender, driver_type):
    driver_df = df[(df['운전자구분'] == driver_type) & (df['성별'] == gender)]
    total_sum = driver_df['종합계'].sum()
    ratio_driver = (total_sum / total_driver) * 100
    return total_sum, ratio_driver

tot_male_regular_sum, ratio_male_regular_driver = calc_tot_and_ratio_by_gender_and_driver_type(ndf, '남', '일반운전자')
tot_female_regular_sum, ratio_female_regular_driver = calc_tot_and_ratio_by_gender_and_driver_type(ndf, '여', '일반운전자')

print("일반운전자 남성 합계:", tot_male_regular_sum)  # 일반운전자 남성 합계: 4558674
print(f"일반운전자 남성 운전자 비율: {ratio_male_regular_driver:.0f}%") # 일반운전자 남성 운전자 비율: 48%

print("일반운전자 여성 합계:", tot_female_regular_sum) # 일반운전자 여성 합계: 3719819
print(f"일반운전자 여성 운전자 비율: {ratio_female_regular_driver:.0f}%") # 일반운전자 여성 운전자 비율: 40%


#%%

# 운전자구분에 따른 전체 운전자 비율
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
labels = ['일반운전자', '노인운전자']
sizes = [tot_regular_driver_sum, tot_elderly_driver_sum]
colors = ['lightgreen', 'lightsalmon']
explode = (0.1, 0)  # 강조를 위한 explode
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('운전자구분 비율(%)')

# 성별에 따른 운전자 구분 비율
plt.subplot(1, 2, 2)
categories = ['노인 여성', '노인 남성', '일반 여성', '일반 남성'] 
ratios = [ratio_elderly_female_driver, ratio_elderly_male_driver, ratio_female_regular_driver, ratio_male_regular_driver]
plt.pie(ratios, labels=categories, autopct='%1.1f%%', startangle=140)
plt.title('성별과 운전자구분 비율(%)')

plt.tight_layout()
plt.show()

#%%
# 성별에 따른 운전자 구분 시각화
# 데이터
categories = ['노인 여성', '노인 남성', '일반 여성', '일반 남성'] # 범주
ratios = [ratio_elderly_female_driver, ratio_elderly_male_driver, ratio_female_regular_driver, ratio_male_regular_driver]

# 비율 막대그래프
plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 2)
plt.bar(categories, ratios, color=['lightcoral', 'lightblue', 'lightcoral', 'lightblue'])
plt.title('성별에 따른 운전자 구분')
plt.xlabel('Category')
plt.ylabel('Ratio (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
