#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("1rec-crime-pfa.csv", parse_dates=["12 months ending"])
df


# In[2]:


offences_stat = {"min": df["Rolling year total number of offences"].min(), 
            "max": df["Rolling year total number of offences"].max(), 
            "mean": df["Rolling year total number of offences"].mean(),
            "median": df["Rolling year total number of offences"].median(),
            "mode": df["Rolling year total number of offences"].mode().to_list(),
            "var": df["Rolling year total number of offences"].var(ddof=0),
            "std": df["Rolling year total number of offences"].std(ddof=0),
            "range": df["Rolling year total number of offences"].max() - df["Rolling year total number of offences"].min(),
            "interquartile_range": df["Rolling year total number of offences"].quantile(0.75) - df["Rolling year total number of offences"].quantile(0.25),
            "skew": df["Rolling year total number of offences"].skew()
            }
offences_stat


# Видим отрицательные значения, но количество преступлений не может быть отрицательным. Скорее всего, это опечатка, возьмём значения по модулю.

# In[128]:


df["Rolling year total number of offences"] = df["Rolling year total number of offences"].abs()


# In[153]:


df["Rolling year total number of offences"].min(), 


# In[130]:


df['Region'].unique()


# In[131]:


cols = list(df.columns)
nom_cols_data = [{name: df[col].to_list().count(name) for name in df[col].unique()}
                 for col in cols
                 if df[col].dtype == "object"]
nom_cols_data


# Видим странные данные, которые встречаются лишь в 31 строчке, тогда как другие исчисляются тысячами. А так же они записаны во всех колонках одинакого. Посмотрим на них внимательнее

# In[132]:


same_df = df.loc[df["PFA"] == df["Offence"]]
same_df


# Видим очень странные данные, которые начинаются лишь с 2011 года, хотя датасет ведётся с 2003 г. Во всех трёх столбцах по-сути записано одно и то же. Погуглив, узнаём, что Action Fraud - это национальное бюро по расследованию случаев мошенничества - это полицейское подразделение в Соединенном Королевстве, которое занимается сбором и анализом разведывательных данных, касающихся мошенничества и киберпреступлений, мотивированных в финансовом отношении. CIFAS - это служба предотвращения мошенничества в Великобритании. Это некоммерческая членская ассоциация, представляющая организации из государственного, частного и добровольного секторов. UK Finance - это торговая ассоциация для сектора банковских и финансовых услуг Великобритании, образованная 1 июля 2017 года. Она представляет около 300 фирм в Великобритании, предоставляющих кредитные, банковские, рыночные и платежные услуги. По всей видимости, это организации, составляющие свою статистику по преступлению мошенничество. Очень не удобных данные, особенно не понятна ситуация с UK Finance, потому что основана на в 2017 году, а данные о преступлениях есть с 2011.

# In[134]:


df = df.loc[(df["PFA"] != "Action Fraud") & (df["PFA"] != "CIFAS") & (df["PFA"] != "UK Finance")]
cols = list(df.columns)
nom_cols_data = [{name: df[col].to_list().count(name) for name in df[col].unique()}
                 for col in cols
                 if df[col].dtype == "object"]
nom_cols_data


# In[135]:


df


# In[137]:


dfch = pd.read_excel("population.xlsx", parse_dates=["12 months ending"])
dfch


# В эту таблицу не попал регион "Британская транспортная полиция", потому что, это, собственно, и не регион. Придётся также избавиться от этих данных.

# In[138]:


df = pd.merge(df, dfch, on=("Region", "12 months ending"))
df


# In[139]:


df['Region'].unique()


# In[149]:


df1 = df.copy()


# In[150]:


df1["Rolling year total number of offences"] = df1["Rolling year total number of offences"]/df1["Population"] * 1000
df1


# In[ ]:




