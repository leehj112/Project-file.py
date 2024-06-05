# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:26:25 2024

@author: dlgur
"""


# 라이브러리 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 시각화하기 위해 폰트 설정
plt.rc('font', family='Malgun Gothic')

# 지역별로 합계와 
ndf['시'].unique()
'''array(['가평', '고양', '과천', '광명', '광주', '구리', '군포', '김포', '남양주', '동두천', '부천',
       '성남', '수원', '시흥', '안산', '안성', '안양', '양주', '양평', '여주', '연천', '오산',
       '용인', '의왕', '의정부', '이천', '파주', '평택', '포천', '하남', '화성'],
      dtype=object)'''

count_unique = ndf['시'].nunique()
print("시 값의 개수:", count_unique) # 시 값의 개수: 31

# 지역(시)에 따른 합계와 비율
def calc_tot_and_ratio_by_region(ndf, region):
    region_df = ndf[ndf['시'] == region]  # 해당 지역만 필터링
    group_tot_sum = region_df.groupby('집계월')['종합계'].sum()  # 해당 지역의 집계월별 총합
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum()  # 전체 집계월별 총합
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100  # 비율 계산
    return group_tot_sum, group_ratio_driver

for i in ndf.index.unique():
    print(f"집계월: {'i'}")
    for region in ndf['시'].unique():
        group_tot_sum_region, group_ratio_region_driver = calc_tot_and_ratio_by_region(ndf, region)
        print(f"지역: {region}")
        print("지역별 총합:")
        print(group_tot_sum_region)
        print("지역별 비율:")
        print(group_ratio_region_driver)
        print()
        
# 지역별 면허소지자 수를 선 그래프 그리기
def plot_region_data(group_tot_sum_region, region_name):
    plt.plot(group_tot_sum_region.index, group_tot_sum_region.values, label=region_name)

# 선 그래프 설정
plt.figure(figsize=(15, 11))
plt.title("지역별 면허소지자 수")
plt.xlabel("집계월")
plt.ylabel("총합")
plt.grid(True)

# 각 지역에 대한 데이터 그래프 그리기
for region in ndf['시'].unique():
    group_tot_sum_region, _ = calc_tot_and_ratio_by_region(ndf, region)
    plot_region_data(group_tot_sum_region, region)

# 범례 표시
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# 그래프 출력
plt.show()

#%%

# 지역(시)에 따른 합계와 비율 계산 함수
def calc_tot_and_ratio_by_region_sw(ndf, region1):
    region_df = ndf[ndf['시'] == region1]  # 해당 지역만 필터링
    group_tot_sum = region_df.groupby('집계월')['종합계'].sum()  # 해당 지역의 집계월별 총합
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum()  # 전체 집계월별 총합
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100  # 비율 계산
    return group_tot_sum, group_ratio_driver

# 수원 지역에 대한 합계와 비율 출력
region1 = '수원'
group_tot_sum_region_sw, group_ratio_region_sw = calc_tot_and_ratio_by_region_sw(ndf, region1)
print(f"{region} 지역의 총합:")
print(group_tot_sum_region_sw)
print(f"{region} 지역의 비율:")
print(group_ratio_region_sw)
'''
수원 지역의 비율:
집계월
201912말    9.169380
202012말    8.985899
202112말    8.882110
202212말    8.921179
202312말    8.951416
202404말    8.938662
Name: 종합계, dtype: float64
'''

# 운전자구분과 성별 매칭하여 합계와 비율 계산하는 함수
def calc_tot_by_gender_and_driver_type(ndf, gender, driver_type):
    driver_df = ndf[(ndf['운전자구분'] == driver_type) & (ndf['성별'] == gender)]  # 운전자구분과 성별에 따라 데이터 필터링
    group_tot_sum = driver_df.groupby('집계월')['종합계'].sum()  # 집계월별 합계 계산
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum()  # 전체 집계월별 총합
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100  # 비율 계산
    return group_tot_sum, group_ratio_driver

# '수원' 지역과 결합하여 계산
tot_regular_female_sum_sw, ratio_regular_female_driver_sw = calc_tot_by_gender_and_driver_type(ndf[ndf['시'] == '수원'], '여', '일반운전자')
tot_regular_male_sum_sw, ratio_regular_male_driver_sw = calc_tot_by_gender_and_driver_type(ndf[ndf['시'] == '수원'], '남', '일반운전자')

print("수원 지역의 여성 일반운전자 합계:", tot_regular_female_sum_sw) 
print("수원 지역의 남성 일반운전자 합계:", tot_regular_male_sum_sw)  

print(f"수원 지역의 여성 일반운전자 비율: {ratio_regular_female_driver_sw.round(1).values}%")
# 수원 지역의 여성 일반운전자 비율: [41.2 41.1 41.1 41.  40.8 40.8]%
print(f"수원 지역의 남성 일반운전자 비율: {ratio_regular_male_driver_sw.round(1).values}%")
# 수원 지역의 남성 일반운전자 비율: [52.2 51.6 51.  50.4 49.8 49.6]%


# 운전자구분과 성별 매칭하여 합계와 비율 계산하는 함수
def calc_tot_by_gender_and_driver_type(ndf, gender, driver_type):
    driver_df = ndf[(ndf['운전자구분'] == driver_type) & (ndf['성별'] == gender)]  # 운전자구분과 성별에 따라 데이터 필터링
    group_tot_sum = driver_df.groupby('집계월')['종합계'].sum()  # 집계월별 합계 계산
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum()  # 전체 집계월별 총합
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100  # 비율 계산
    return group_tot_sum, group_ratio_driver

# '수원' 지역과 결합하여 계산
tot_elderly_female_sum_sw, ratio_elderly_female_driver_sw = calc_tot_by_gender_and_driver_type(ndf[ndf['시'] == '수원'], '여', '노인운전자')
tot_elderly_male_sum_sw, ratio_elderly_male_driver_sw = calc_tot_by_gender_and_driver_type(ndf[ndf['시'] == '수원'], '남', '노인운전자')

print("수원 지역의 여성 노인운전자 합계:", tot_elderly_female_sum_sw) 
print("수원 지역의 남성 노인운전자 합계:", tot_elderly_male_sum_sw)  

print(f"수원 지역의 여성 노인운전자 비율: {ratio_elderly_female_driver_sw.round(1).values}%")
# 수원 지역의 여성 노인운전자 비율: [1.8 2.1 2.4 2.8 3.1 3.2]%
print(f"수원 지역의 남성 노인운전자 비율: {ratio_elderly_male_driver_sw.round(1).values}%")
# 수원 지역의 남성 노인운전자 비율: [4.8 5.2 5.5 5.8 6.2 6.4]%


#%%
# 수원시 일반운전자와 노인운전자 성별 구분 그래프(합계)
plt.figure(figsize=(14, 10))

# 여성과 남성 일반운전자 비율 그래프
plt.subplot(2, 1, 1)
plt.plot(tot_regular_female_sum_sw.index, tot_regular_female_sum_sw.values, marker='o', label='여성')
plt.plot(tot_regular_male_sum_sw.index, tot_regular_male_sum_sw.values, marker='o', label='남성')
plt.title('수원 지역 일반운전자 성별 합계')
plt.xlabel('집계월')
plt.ylabel('합계')
plt.legend()

# 여성과 남성 노인운전자 비율 그래프
plt.subplot(2, 1, 2)
plt.plot(tot_elderly_female_sum_sw.index, tot_elderly_female_sum_sw.values, marker='o', label='여성')
plt.plot(tot_elderly_male_sum_sw.index, tot_elderly_male_sum_sw.values, marker='o', label='남성')
plt.title('수원 지역 노인운전자 성별 합계')
plt.xlabel('집계월')
plt.ylabel('합계')
plt.legend()

plt.tight_layout()
plt.show()

#%%
# 수원시 일반운전자와 노인운전자 성별 구분 그래프(비율)
plt.figure(figsize=(14, 10))

# 여성과 남성 일반운전자 비율 그래프
plt.subplot(2, 1, 1)
plt.plot(ratio_regular_female_driver_sw.index, ratio_regular_female_driver_sw.values, marker='o', label='여성')
plt.plot(ratio_regular_male_driver_sw.index, ratio_regular_male_driver_sw.values, marker='o', label='남성')
plt.title('수원 지역 일반운전자 성별 비율(%)')
plt.xlabel('집계월')
plt.ylabel('비율')
plt.legend()

# 여성과 남성 노인운전자 비율 그래프
plt.subplot(2, 1, 2)
plt.plot(ratio_elderly_female_driver_sw.index, ratio_elderly_female_driver_sw.values, marker='o', label='여성')
plt.plot(ratio_elderly_male_driver_sw.index, ratio_elderly_male_driver_sw.values, marker='o', label='남성')
plt.title('수원 지역 노인운전자 성별 비율(%)')
plt.xlabel('집계월')
plt.ylabel('비율')
plt.legend()

plt.tight_layout()
plt.show()

#%%


# 상위 그래프 하나로 통일
plt.figure(figsize=(10, 6))

# 여성과 남성 일반운전자 비율 그래프
plt.plot(ratio_regular_female_driver_sw.index, ratio_regular_female_driver_sw.values, marker='o', label='일반 여성')
plt.plot(ratio_regular_male_driver_sw.index, ratio_regular_male_driver_sw.values, marker='o', label='일반 남성')

# 여성과 남성 노인운전자 비율 그래프
plt.plot(ratio_elderly_female_driver_sw.index, ratio_elderly_female_driver_sw.values, marker='o', linestyle='--', label='노인 여성')
plt.plot(ratio_elderly_male_driver_sw.index, ratio_elderly_male_driver_sw.values, marker='o', linestyle='--', label='노인 남성')

plt.title('수원 지역 성별에 따른 일반운전자와 노인운전자 비율(%)')
plt.xlabel('집계월')
plt.ylabel('비율')
plt.legend()

plt.show()

#%%
# 수원지역의 전체 면허소지자 수와 성별과 운전자구분으로 그래프 그리기 
# 그래프 생성
fig, ax1 = plt.subplots(figsize=(10, 6))

# 비율 그래프 (라인 그래프)
ax1.plot(tot_regular_female_sum_sw.index, tot_regular_female_sum_sw.values, marker='o', label='일반 여성')
ax1.plot(tot_regular_male_sum_sw.index, tot_regular_male_sum_sw.values, marker='o', label='일반 남성')
ax1.plot(tot_elderly_female_sum_sw.index, tot_elderly_female_sum_sw.values, marker='o', linestyle='--', label='노인 여성')
ax1.plot(tot_elderly_male_sum_sw.index, tot_elderly_male_sum_sw.values, marker='o', linestyle='--', label='노인 남성')

# 전체 운전자수 막대 그래프 (투명도를 적용하여 선 그래프와 겹치지 않게)
ax1.bar(group_tot_sum_region_sw.index, group_tot_sum_region_sw.values, alpha=0.3, color='gray', label='전체 운전자 수')

ax1.set_title('수원 지역 면허소지자 현황')
ax1.set_xlabel('집계월')
ax1.set_ylabel('운전자수')
ax1.legend(loc='upper left')

plt.show()