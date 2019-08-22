import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mode
from datetime import datetime
import time

st = time.time()


warnings.filterwarnings("ignore", category=FutureWarning)
sns.set()



train = pd.read_excel("all_fb_ads.xlsx") 

print (train.info())

print (train.apply(lambda x: sum(x.isnull())))
print (train.describe())
print (train.apply(lambda x: len(x.unique())))

## Removing Nan and handling missing values

train["adText"].fillna("No Text", inplace=True)
train["adLP"].fillna("none", inplace=True)
train['adClicks'].fillna(0, inplace=True)
train['adImpress'].fillna(train['adClicks'], inplace=True)
train["groups"].fillna("Not known", inplace=True)
train['adLocation_cleaned'].fillna(" ", inplace=True)
train['adStates'].fillna(" ", inplace=True)
train['adCreation'].fillna("", inplace=True)

adCreat = train['adCreation']
a = adCreat.copy()

for ind in adCreat.index:

	a[ind] = str(a[ind]).replace(" ","")
	a[ind] = str(a[ind]).replace("-",":")

	a[ind] = "01/01/17" if (a[ind] == "" or (a[ind][0] != '0' and a[ind][0] != '1')) else a[ind][0:9] if ('&' in a[ind]) else a[ind]
	

	if (len(a[ind])>=len(a[1])-1) and ((a[ind][-8])!=":"):
		alist = list(a[ind])
		alist.insert(13, ':')
		a[ind] = "".join(alist)

## Spliting adCreation into adDate and Time


train['adDate'] = ([a[i][0:8] for i in a.index])
for i in train.index:
	try:
		train['adDate'][i] =  pd.to_datetime(train['adDate'][i], format='%m/%d/%y')
	except ValueError:
		train['adDate'][i] =  pd.to_datetime("01/01/17", format='%m/%d/%y')
		print (train['adDate'][i])
train['Time'] = ([a[i][8:] for i in a.index])
temp = train['Time'].copy()

tlen = len(train['Time'][1])

## Saving time as hours
for i in train.index:
	if  (len(train['Time'][i])>=tlen):
		temp[i] = train['Time'][i].replace(train['Time'][i][0:2],str(int(train['Time'][i][0:2])+12)) if (train['Time'][i][8] == 'P') else train['Time'][i]

train['Time'] = temp

train['Time'] = ([train['Time'][i][:2] for i in a.index])
train['Time'] = pd.to_numeric(train['Time'])

## Saving days as number of days prior to the election
ele_date = datetime.strptime('11/08/16', '%m/%d/%y')
train['days'] = (ele_date - train['adDate'])

train['days'] = [(train['days'].loc[i]).days for i in range(len(train['days']))]

train.drop(['adCreation', 'adDate', 'adID'], axis=1, inplace=True)

## Convertion adtext to class based on the words in text

a = train['adText']

word_list = ['Trump', 'wall', 'war', 'politics', 'racism', 'Clinton', 'liberty', 'black', 'rally', 'election', 'president', 'ISIS', 'Syria', 'terror']
train['adText'] = [int(any(s in a[i] for s in word_list)) for i in range(len(a))]


train['adLP'] = ['none' if train['adLP'][i].find('.com') < 0 else train['adLP'][i][0:train['adLP'][i].find('.com')+4] for i in range(len(train['adLP']))]

## Cleaning duplicated in url

train['adLP'] = train['adLP'].replace({'https://instagram.com':'https://www.instagram.com', 'https:Hinstagram.com':'https://www.instagram.com',
							'https:Hblackmattersus.com':'https://blackmattersus.com', 'https:Hblackm attersus.com':'https://blackmattersus.com',
							'https:Hrepresent.com':'https://represent.com', 'https://www .facebook.com':'https://www.facebook.com', 
							'https://\\vww.facebook.com':'https://www .facebook.com', 'https://www,facebook.com':'https://www .facebook.com'	})


## Separating the states
col1 = []
for i in train['adStates']:
	col1 = col1 + i.split()


for i in range(len(col1)):
	if any(s in col1[i] for s in ['New', 'South', 'North']):
		col1[i] = col1[i] + " " + col1[i+1]
		col1[i+1] = " "


col1 = [x for x in col1 if x != " "]
col1 = list(set(col1))

for i in col1:
	train[i] = 0
print (train.shape)
# row = [x for x in train.index if train['adStates'][x] != " "]
temp = []
for idx in train.index:

	state = train['adStates'][idx].split()
		
	if any(s in state for s in ['New', 'South', 'North']):

		ind = state.index('New') if 'New' in state else state.index('South') if 'South' in state else state.index('North')
		state[ind] = state[ind] + " " + state[ind+1]
		state[ind+1] = ""
	# for i in col1:
	# 	train[i].loc[idx] = int(i in state)

	temp.append([int(i in state) for i in col1])
	
train[col1] = temp


state_count = [train[c].sum() for c in col1]


train.drop(['adLocation_cleaned', 'adStates'], axis=1, inplace=True)


train.fillna(0, inplace=True)

train.to_csv("cleaned_all_fb_ads.csv")

## PLOT


val_col = ['adSpend', 'adImpress', 'adClicks', 'Time', 'days']


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


for col in ['adSpend', 'adImpress', 'adClicks']:
	train[col]= pd.DataFrame(scaler.fit_transform(pd.DataFrame(train[col]))).round(2)


for col in val_col:
	df = train.groupby(col)[col].count()
	df = pd.DataFrame({col:df.index, 'count':df.values})

	df.plot(kind='line',x=col,y="count")


fig = plt.figure(len(val_col)+1)
plt.bar(col1, state_count)

plt.xticks(rotation=90)

df = train.groupby('adLP')['adLP'].count()
df = pd.DataFrame({'adLP':df.index, 'count':df.values})
df.plot(kind='bar',x='adLP',y="count")


rows = [x for x in train.index if train['adText'][x] == 1]
train1 = train.loc[rows]

for col in val_col:
	df = train1.groupby(col)[col].count()
	df = pd.DataFrame({col:df.index, 'count':df.values})

	df.plot(kind='line',x=col,y="count")


df = train1.groupby('adLP')['adLP'].count()
df = pd.DataFrame({'adLP':df.index, 'count':df.values})
df.plot(kind='bar',x='adLP',y="count")


plt.show()

print("--- %s seconds ---" % (time.time() - st))