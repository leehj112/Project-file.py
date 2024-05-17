# -*- coding: utf-8 -*-
"""
Created on Fri May 17 18:47:56 2024

@author: dlgur
"""


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


url='https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt'
response=requests.get(url)
data=pd.read_csv(url,delimiter='\t')
print(data.head())


#bmi 와 y(target) 의 관계 시각화
sns.scatterplot(x='BMI',y='Y',data=data)
plt.xlabel("bmi")
plt.ylabel("progression of diabetes")
plt.title("relationship between bmi & progression of diabetes")
plt.show()

#선형회귀이용해서 당뇨진행정도 예측

from sklearn.linear_model import LinearRegression

diabetes=data
x=diabetes['BMI']       #독립변수(X) BMI
y=diabetes['Y']         #종속변수(Y) Y

model=LinearRegression()
x=x.values.reshape(-1,1)    #1차원배열을 2차원배열로
model.fit(x,y)

print("기울기:",model.coef_[0])
print("x절편(intercept):",model.intercept_)
#-> 머신러닝 모델 : y=10.2x+(-117.8)

#선형회귀 시각화
plt.scatter(x,y,alpha=0.5)
plt.plot(x,model.predict(x),color='red',linewidth=2)
plt.xlabel("bmi")
plt.ylabel("progression of diabetes")
plt.title("linear regression(bmi & y)")
plt.show()