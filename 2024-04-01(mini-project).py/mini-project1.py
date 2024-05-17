# -*- coding: utf-8 -*-
"""
Created on Fri May 17 18:47:45 2024

@author: dlgur
"""


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

#데이터 준비
url='https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt'
response=requests.get(url)
data=pd.read_csv(url,delimiter='\t')
print(data.head())

"""
age (나이): 환자의 나이
sex (성별): 환자의 성별 (남성은 1, 여성은 0)
bmi (체질량 지수): 환자의 체질량 지수
bp (평균 혈압): 환자의 평균 혈압
s1 (혈청 검사 1): 총 혈청 콜레스테롤
s2 (혈청 검사 2): 저밀도 지단백
s3 (혈청 검사 3): 고밀도 지단백
s4 (혈청 검사 4): 총 콜레스테롤 / HDL 비율
s5 (혈청 검사 5): 혈청 트리글리세라이드의 로그
s6 (혈청 검사 6): 혈당 수준
y  당뇨병 진행상태를 나타냄,
    기준 이후 1년간의 질병 진행의 양적 측정값,관심 대상인 질병 진행의 양적 지표로 사용
    당뇨병 환자의 질병 상태의 진행을 나타내며, 다양한 요인들과의 상관 관계나 예측 모델링 등의 분석에 사용."""

#데이터 탐색
print(data.describe())
print(data.info())          #NULL값 없음

#데이터 상관관계분석
correlation_matrix=data.corr()
print(correlation_matrix)

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()
#%% 
#변수분포 히스토그램
data.hist(figsize=(12,10))
plt.tight_layout()
plt.show()

#bmi지수와 y는 연관이있는가?/

from sklearn.model_selection import train_test_split
train_set,test_set=train_test_split(data,random_state=42)       #75:25(3:1)
print(len(train_set),len(test_set))             #331 111

x_train=train_set[['BMI']]                      #독립변수 x
y_train=train_set['Y']                          #종속변수 y

print(x_train.shape,y_train.shape)              #(331, 1) (331,)  ->2차원배열,1차원배열

#선형회귀모델 훈련하기
from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(x_train,y_train)


#훈련된 모델을 평가하기:결정계수
x_test=test_set[['BMI']]
y_test=test_set['Y']
lr.score(x_test,y_test)             #Out[176]: 0.31720994495377797  ->결정계수 0.32 이므로 모형의 예측능력낮음

#연속적인 값 예측하기:선형회귀
print(lr.coef_,lr.intercept_)       #[10.51165308] -125.17664066850949


#카테고리 예측하기:로지스틱 회귀
y_mean=data['Y'].mean()
print(y_mean)

y_train_c=y_train>y_mean
y_test_c=y_test>y_mean              #평균 당수치 보다 높으면 True


from sklearn.linear_model import LogisticRegression
logr=LogisticRegression()
logr.fit(x_train,y_train_c)
logr.score(x_test,y_test_c)         #Out[186]: 0.7027027027027027  //나름 괜찮은 결과

#양성클래스,음성클래스 분포확인
y_test_c.value_counts()
"""
Y
False    64
True     47
Name: count, dtype: int64 """ #  48%:42% 이므로 균형한 데이터임을 확인

from sklearn.dummy import DummyClassifier

dc=DummyClassifier()
dc.fit(x_train,y_train_c)
dc.score(x_test,y_test_c)       # 0.5765765765765766  적어도 58보다 커야지 유용한 모델이다


#단순회귀분석
data.plot(kind='scatter',x='BMI',y='Y',figsize=(10,5)) #bmi클수록 당수치 높음
plt.show()
plt.close()

"""
grid_ndf=sns.pairplot(data)
plt.show()
plt.close() """

#의사결정트리
#속성(변수) 선택
x=data.drop(columns=['Y'])
y=data['Y']

#설명변수 데이터 정규화
from sklearn import preprocessing
x=preprocessing.StandardScaler().fit(x).transform(x)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42)

print(x_train.shape,x_test.shape)       #(331, 10) (111, 10)  ->3:1비율

#모형 학습 및 검증
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

tree_model=tree.DecisionTreeClassifier(criterion='entropy',max_depth=5)

tree_model.fit(x_train,y_train)

y_hat=tree_model.predict(x_test)

print(y_hat[:10])
print(y_test.values[:10])

from sklearn import metrics

tree_matrix=metrics.confusion_matrix(y_test,y_hat)
print(tree_matrix)

tree_report=metrics.classification_report(y_test,y_hat,zero_division=1)
print(tree_report)

# 결정 트리 모델 훈련
tree_model = DecisionTreeRegressor(random_state=42)
tree_model.fit(x_train, y_train)

# 모델 평가
y_pred = tree_model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)        #평균제곱오차
print("Mean Squared Error:", mse)               #Mean Squared Error: 5807.7027027027025



tree_matrix=metrics.confusion_matrix(y_test,y_pred)
print(tree_matrix)

tree_report=metrics.classification_report(y_test,y_hat,zero_division=1)
print(tree_report)

#%%

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import requests

# 데이터 불러오기
url = 'https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt'
response = requests.get(url)
data = pd.read_csv(url, delimiter='\t')

# 독립 변수와 종속 변수 설정
x = data.drop(columns=['Y'])
y = data['Y']

# 독립 변수 데이터 정규화
x = StandardScaler().fit(x).transform(x)

# 데이터 분할
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 의사결정트리 분류 모델 학습
tree_classifier = DecisionTreeClassifier(criterion='entropy', max_depth=5)
tree_classifier.fit(x_train, y_train)

# 의사결정트리 회귀 모델 학습
tree_regressor = DecisionTreeRegressor(random_state=42)
tree_regressor.fit(x_train, y_train)

# 분류 모델 평가
y_pred_classifier = tree_classifier.predict(x_test)
tree_matrix_classifier = confusion_matrix(y_test, y_pred_classifier)
tree_report_classifier = classification_report(y_test, y_pred_classifier, zero_division=1)

# 회귀 모델 평가
y_pred_regressor = tree_regressor.predict(x_test)
mse_regressor = mean_squared_error(y_test, y_pred_regressor)

print("Decision Tree Classification Results:")
print("Confusion Matrix:\n", tree_matrix_classifier)
print("Classification Report:\n", tree_report_classifier)

print("\nDecision Tree Regression Results:")
print("Mean Squared Error:", mse_regressor)