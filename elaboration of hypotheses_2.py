#!/usr/bin/env python
# coding: utf-8

# In[99]:


import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
df = pd.read_csv("1rec-crime-pfa.csv", parse_dates=["12 months ending"])
df


# In[100]:


dfch = pd.read_excel("population.xlsx", parse_dates=["12 months ending"])
df_new = pd.merge(df, dfch, on=("Region", "12 months ending"))
df_new["number of offences per 1000 people"] = df_new["Rolling year total number of offences"]/df_new["Population"] * 1000
df_new


# 1 Гипотеза: Удаление данных организаций не сильно отразится на общую картину распределения преступлений. 
# Сначала покажем общее распределение преступлений с течением времени до обработки.

# In[101]:


time_offence = df.groupby("12 months ending").sum()["Rolling year total number of offences"]
fig_time_offence = px.line(time_offence, y="Rolling year total number of offences")
fig_time_offence.show()


# После удаления неудобных данных распределение приняло следующий вид:

# In[102]:


time_offence_new = df_new.groupby("12 months ending").sum()["Rolling year total number of offences"]
fig_time_offence_new = px.line(time_offence_new, y="Rolling year total number of offences")
fig_time_offence_new.show()


# По всей видимости, мы нашли объяснение двойному минимуму распределения преступлений. Он появлялся только из-за внезапного появления в середине 2011 года новых строк с данными от частных организаций. Однако возрастание преступности, начиная с 2014 года никуда не делся. В целом можно заключить, что гипотеза почти подтвердилась.

# 2 Гипотеза: Нормировка преступлений гораздо точнее покажет опасность отдельных районов. Сначала покажем общее распределение преступлений по регионам до обработки.

# In[103]:


Region_offence = df_new.groupby("Region").sum()["Rolling year total number of offences"].sort_values()
fig_Region_offence = px.bar(Region_offence, y='Rolling year total number of offences')
fig_Region_offence.show()


# Теперь покажем распределение преступлений с учётом количества жителей в регионах.

# In[104]:


Region_offence_new = df_new.groupby("Region").sum()["number of offences per 1000 people"].sort_values()
fig_Region_offence_new = px.bar(Region_offence_new, y='number of offences per 1000 people')
fig_Region_offence_new.show()


# Хоть Лондон и оставил за собой криминальное лидерство, можно заметить существенные изменения в распределении преступлений. Так Северо-Восточный округ с последнего 10 места переместился аж на 4, а Юго-Восточный со 2 на 8 место. Но, что самое главное, теперь распределение приблизилось к равномерному, то есть на самом деле в стране нет такого сильного криминогенного перекоса. Гипотеза полностью подтвердилась.

# 3 Гипотеза: В зоне ответственности столичной полиции криминальная обстановка не настолько сильно отличается относительно других районов, если сделать поправку на количество жителей, которое они обхватывают. Покажем, какое распределение мы видели во 2 задании.

# In[105]:


PFA_offence = df_new.groupby("PFA").sum()["Rolling year total number of offences"].sort_values()
fig_PFA_offence = px.bar(PFA_offence, y='Rolling year total number of offences')
fig_PFA_offence.show()


# С поправкой на население распределение принимает следующий вид:

# In[106]:


PFA_offence_new = df_new.groupby("PFA").sum()["number of offences per 1000 people"].sort_values()
fig_PFA_offence_new = px.bar(PFA_offence_new, y='number of offences per 1000 people')
fig_PFA_offence_new.show()


# Видим, что некоторые районы сместились, например Northumbria с 15 места поднялась на 3. Но общая картина распределения практически не изменилась и столичная полиция лидирует с большим отрывом. Следовательно гипотеза не подтвердилась.

# Гипотеза 4. У разных полицейских участков сильно отличается количество подкотрольных им регионов. Так как полицейских участков намного больше, чем регионов, корректнее было бы сформулировать гипотезу наоборот: в разных регионах количество полицейских отделов сильно разнится.

# In[107]:


for i in df_new.Region.unique():
  print(i, 
        df_new["PFA"].loc[df_new["Region"] == i].unique())


# Можно, конечно, отобразить, как было изначально сформулировано, но так менее наглядно. Зато отчётливо видно, что ни один полицейский участок не дежурит сразу в нескольких регионах страны.

# In[108]:


for i in df_new.PFA.unique():
  print(i, 
        df_new["Region"].loc[df_new["PFA"] == i].unique())


# Видим, что количество полицейских отделов разнится от 2 в Лондоне до 6 в Восточном округе. Из этой картины мы понимаем, почему на графике преступлений по районам столичная полиция имеет такой выброс. Там всего 2 участка, 1 из которых вообще почти не имеет (или не выкладывает) преступлений. Получается всего один участок на самый крупный регион страны. Можно заключить, что гипотеза скорее подтвердилась.

# 5 Гипотеза: возможно, уровень преступности как-то коррелирует с широтами, в которых находится регион, например, чем южнее, тем больше в среднем совершается в год преступлений.

# In[109]:


df_Region_offence_new = pd.DataFrame(Region_offence_new)
df_Region_offence_new.reset_index()


# In[110]:


df_Region_offence_new.dtypes


# In[111]:


from urllib.request import urlopen
import json
with urlopen('https://martinjc.github.io/UK-GeoJSON/json/eng/topo_eer.json') as response:
    UK = json.load(response)
UK['objects']['eer']['geometries'][0]['properties']


# In[112]:


fig = px.choropleth(df_Region_offence_new, geojson=UK, locations='Region', 
                    featureidkey="properties.EER13NM",
                    color='number of offences per 1000 people',
                           color_continuous_scale="tealrose",
                           scope = "europe",
                           range_color=(0, 10),
                           labels={'number':'number of offences per 1000 people'},
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# Я не понимаю...

# In[113]:


list1 = ["South West", "East", "South East", "Wales", "West Midlands", "East Midlands", "North East", "North West", "Yorkshire and The Humber", "London"]
list2 = [3321, 3321, 3501, 3565, 3678, 3743, 3842, 4190, 4406, 5123]
df_Region_offence = pd.DataFrame({'Region' : list1, 'number of offences per 1000 people' : list2})
df_Region_offence


# In[114]:


df_Region_offence.dtypes


# In[115]:


fig = px.choropleth(df_Region_offence, geojson=UK, locations='Region', 
                    featureidkey="properties.EER13NM",
                    color='number of offences per 1000 people',
                           color_continuous_scale="tealrose",
                           scope = "europe",
                           range_color=(0, 5000),
                           labels={'number':'number of offences per 1000 people'},
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# In[ ]:




