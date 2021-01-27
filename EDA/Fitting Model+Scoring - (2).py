#!/usr/bin/env python
# coding: utf-8

# In[216]:


import pandas as pd
import matplotlib.pyplot as plt


# In[217]:


total = pd.read_csv('total_sub.csv',index_col='Unnamed: 0')
total.sample(6) #345,61


# In[218]:


total.columns


# In[219]:


'''
X = pd.DataFrame(total.drop(['gid','geometry','가장동','갈곶동','고현동','궐동','금암동','내삼미동','부산동','누읍동','벌음동','부산동','서동','서랑동',
                                '세교동','수청동','양산동','오산동','외삼미동','원동','은계동','지곶동','청학동','청호동','탑동',
                                '광성초양산초병점초공동통학구역','광성초통학구역','금암초통학구역','대호초성산초공동통학구역',
                                '대호초통학구역','매홀초삼미분교수청초필봉초공동통학구역','매홀초삼미분교장통학구역','매홀초통학구역',
                                '문시초통학구역','성산초통학구역','성호초운암초공동통학구역','성호초통학구역','세미초통학구역','수청초통학구역',
                                '양산초통학구역', '오산고현초오산원당초공동통학구역','오산고현초통학구역','오산대원초원동초공동통학구역','오산대원초통학구역',
                                '오산원당초통학구역','오산원일초통학구역','오산초가수초공동통학구역','오산초통학구역','운산초통학구역','운암초통학구역',
                                '원동초통학구역','필봉초통학구역','화성초통학구역'],axis=1))
'''
X = pd.DataFrame(total.drop(['accident_cnt'],axis=1))
cols = X.columns
Y = pd.Series(total["accident_cnt"])
X.shape , Y.shape


# ### - split validation set

# In[220]:


from sklearn.preprocessing import MinMaxScaler , StandardScaler
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
m_scaler = MinMaxScaler()
X = scaler.fit_transform(X)

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=2021)
x_train.shape , x_test.shape


# In[221]:


from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error,make_scorer
from sklearn.model_selection import cross_val_score


# In[222]:


my_scorer = make_scorer(mean_squared_error,greater_is_better=False)

kf = KFold(n_splits=10,shuffle=True,random_state=2021)


# ## Fitting AdaBoost Model

# In[223]:


from sklearn.ensemble import AdaBoostRegressor

ada = AdaBoostRegressor(n_estimators=200,learning_rate=0.1,loss="linear",random_state=2021)
ada.fit(x_train, y_train)

Rscore = ada.score(x_test,y_test)
score = cross_val_score(ada,x_test,y_test,cv=kf,scoring=my_scorer)  
print("MSE :",score.mean()*(-1))


# In[224]:


from sklearn.ensemble import AdaBoostRegressor

ada = AdaBoostRegressor(n_estimators=200,learning_rate=0.1,loss="exponential",random_state=2021)
ada.fit(x_train, y_train)

Rscore = ada.score(x_test,y_test)
score = cross_val_score(ada,x_test,y_test,cv=kf,scoring=my_scorer)  
print("MSE :",score.mean()*(-1))


# ## Fitting XGBoost Model

# In[227]:


import xgboost
xgb_model = xgboost.XGBRegressor(n_estimators=200, learning_rate=0.08, gamma=0, subsample=0.75,
                           colsample_bytree=1, max_depth=7)

xgb_model.fit(x_train,y_train)

Rscore = xgb_model.score(x_test,y_test)
score = cross_val_score(xgb_model,x_test,y_test,cv=kf,scoring=my_scorer)  
print("MSE :",score.mean()*(-1))


# In[228]:


import matplotlib.pyplot as plt
xgboost.plot_importance(xgb_model)


# ### 전체 모델들의 MSE 시각화

# In[229]:


data = [['Linear Regression',1.0499],['Ridge Regression',0.97336],['Lasso Regression', 0.94607],['Eleastic Regerssion',0.88615],
       ['SVM -linear',1.4186], ['SVM-radial',1.33959],['Regression Tree',0.99607],['Random Forest',0.98421],['Gradient Boosting',1.0391],
       ['AdaBoost',0.47954],['XGBoost', 0.59189]]


# In[230]:


df = pd.DataFrame(data,columns=['Model','MSE'])


# In[231]:


df


# In[232]:


import matplotlib.pyplot as plt


# In[233]:


df2 = df.sort_values(by='MSE',axis=0,ascending=False)


# In[234]:


plt.figure(figsize=(12,8))
plt.bar(df2.Model,df2.MSE, align='edge', color='springgreen',edgecolor="red", linewidth=1.5)
plt.xticks(rotation = 45)


# ##  - Adaboost 모델 성능이 제일 좋다

# In[ ]:





# In[235]:


total = pd.read_csv('total_sub.csv',index_col='Unnamed: 0')
total.head()
#total2.shape (345, 81)
#total2


# In[236]:


X = pd.DataFrame(total.drop(['accident_cnt'],axis=1))
cols = X.columns
Y = pd.Series(total["accident_cnt"])
X.shape , Y.shape


# In[237]:


pred = ada.predict(X)
pred


# In[238]:


temp = pd.read_csv('total_dat.csv')


# In[239]:


total['gid'] = temp.gid


# In[240]:


total['pred_score'] = pred


# In[241]:


total


# In[242]:


candidate = pd.read_csv('candidate_grid2.csv',index_col='Unnamed: 0')
candidate.head()


# In[243]:


total = pd.DataFrame(total.drop(['accident_cnt'],axis=1))
total.head()


# In[244]:


dat = pd.merge(candidate,total,left_on='gid',right_on='gid',how='left')
dat.head()


# In[245]:


dat['total_score']=dat.pred_score-dat.accident_cnt


# In[211]:


dat.to_csv('ada_totalscore.csv')


# In[246]:


top20 = dat.sort_values(by='total_score').head(20)


# In[214]:


top20.to_csv('ada_top_20.csv')


# In[248]:


ada_top20 = top20[['accident_cnt','total_score']]
ada_top20


# In[ ]:





# In[ ]:




