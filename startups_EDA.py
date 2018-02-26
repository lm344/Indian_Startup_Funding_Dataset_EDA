import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from subprocess import check_output

df_startups = pd.read_csv('startup_funding.csv',index_col=0)

#Knowing our data
print(df_startups.shape)
print(df_startups.nunique())
print(df_startups.info())

#Using Head to look for data
print(df_startups.head())

#EDA with amount distributions
df_startups["AmountInUSD"] = df_startups["AmountInUSD"].apply(lambda x: float(str(x).replace(",","")))

print("Min Amount")
print(df_startups["AmountInUSD"].min())
print("Mean Amount")
print(round(df_startups["AmountInUSD"].mean(),2))
print("Median Amount")
print(df_startups["AmountInUSD"].median())
print("Max Amount")
print(df_startups["AmountInUSD"].max())
print("Standard Deviation Amount")
print(round(df_startups["AmountInUSD"].std(),2))



#AmountInUSD has some null values. Replace null values with mean
mean_of_amount = int(np.mean(df_startups['AmountInUSD']))
df_startups['AmountInUSD'] = df_startups['AmountInUSD'].apply(lambda x:mean_of_amount if x == 0 else x )

#Checking for NaN's
print("NaN's description")
print(df_startups.isnull().sum())

#Extracting Year from Data column and added in to new column called 'YEAR'
df_startups['Date'] = df_startups['Date'].apply(lambda dt:dt.replace(".","/"))
df_startups['Date'] = df_startups['Date'].apply(lambda dt:dt.replace("//","/"))
df_startups['Date'] = pd.to_datetime(df_startups['Date'],dayfirst=True)
df_startups['year'] = df_startups['Date'].apply(lambda dt:dt.year)

#Check whether new column is added
df_startups.info()

#The dataset has data for three years only
print(df_startups['year'].value_counts())

#Get count of startups which received funding group by year
by_year_cmp = df_startups[['StartupName','year']].groupby(by='year').count()

#Plot no.of companies which received funding groupby year
sns.barplot(x='year',y='StartupName',data=by_year_cmp.reset_index())
plt.title('No.of startups which received funding group by year')
plt.xlabel('Year')
plt.ylabel('Count of startups')
plt.tight_layout()
plt.show()

#2016 was the year when most startups received funding

#Now let us explore the importance of location in the funding. Since there will be many locations, we could just try to plot the top 10 locations.
location = df_startups['CityLocation'].value_counts()
print("Description count of Location")
print(location[:15])

plt.figure(figsize=(12,6))
sns.barplot(x=location.index[:20], y=location.values[:20])
plt.xticks(rotation=45)
plt.xlabel('Industry Name', fontsize=12)
plt.ylabel('Industry counting', fontsize=12)
plt.title("Count frequency of Industry ", fontsize=16)
plt.show()

#Bangalore seems to attract lot of investments followed by Mumbai and Delhi.


#Why Bangalore? check this out..?

# nan values in dataset are stored as float datatype. convert them to np.nan so that, it would be easy to remove them
df_startups['CityLocation'] = df_startups['CityLocation'].apply(lambda x:np.nan if str(x) == 'nan' else x)

#Now drop nan values easily
df_startups['CityLocation'] = df_startups['CityLocation'].dropna()

#Create a new dataframe which holds Cities and amount
top_cities_dataframe = df_startups[['CityLocation','AmountInUSD']]
#Group by startupname and retrieve the sum of amounts
top_cities = top_cities_dataframe.groupby(by='CityLocation').sum().astype('int64')
#Sort the calculates sum in descending order
top_cities.sort_values(by='AmountInUSD',ascending=False,inplace=True)

#Plot city and amount
top_cities_name = top_cities.reset_index()[:10]['CityLocation']
top_cities_amount = top_cities.reset_index()[:10]['AmountInUSD']
plt.figure(figsize=(12,8))
sns.barplot(y=top_cities_name,x=top_cities_amount)
plt.ylabel('Cities')
plt.xlabel('Average investment amount received (in Millions USD)')
plt.title('Top 10 Cities and average amount received')
plt.show()

#Startups in Bangalore have received highest funding amount


#Which industries are favored by investors for funding?
#We can now explore the Industry vertical information.
industry = df_startups['IndustryVertical'].value_counts()[:20]

plt.figure(figsize=(12,6))
sns.barplot(x=industry.index, y=industry.values)
plt.xticks(rotation=45)
plt.xlabel("Industry's Name", fontsize=12)
plt.ylabel('Industry counting', fontsize=12)
plt.title("Count frequency of Industry Verical", fontsize=16)
plt.show()

#Consumer Internet is the most preferred industry segment for funding followed by Technology and E-commerce.

#Exploring further through industry vertical and its sub verticals
technology_sub = df_startups[df_startups['IndustryVertical'] == 'Technology']['SubVertical'].value_counts()

plt.figure(figsize = (10,6))
graph1 = sns.barplot(x=technology_sub.index[:20],y=technology_sub.values[:20])
graph1.set_xticklabels(graph1.get_xticklabels(),rotation=90)
graph1.set_title("Sub Category's by Technology", fontsize=15)
graph1.set_xlabel("", fontsize=12)
graph1.set_ylabel("Count", fontsize=12)
plt.show()

#Data Analytics platform seems to be the top centender in sub technology category. Interesting Information.

#Drop NA values from investor names and convert the values to upper case
df_startups['InvestorsName'] = df_startups['InvestorsName'].dropna()
investors = df_startups['InvestorsName'].apply(lambda iv:str(iv).upper())
investors_count = investors.value_counts()[:10]
investors = investors.dropna().unique()[:10]

#Plot investor names and count
plt.figure(figsize=(12,8))
sns.barplot(y=investors,x=investors_count)
plt.xticks(rotation=90)
plt.ylabel('Investors')
plt.xlabel('Count')
plt.title('Top 10 Investors and the count of companies')
plt.show()

#KAE capital has invested in highest number of startups

