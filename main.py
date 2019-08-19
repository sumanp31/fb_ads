import warnings
import numpy as np
import pandas as pd
from scipy.stats import mode
# import sklearn as sk

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv("cleaned_all_fb_ads.csv")
cols = df.columns
df = pd.read_csv("cleaned_all_fb_ads.csv", usecols=cols[1:])


## Normalize
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


for col in ['adSpend', 'adImpress', 'adClicks', 'Time', 'days']:
	df[col]= pd.DataFrame(scaler.fit_transform(pd.DataFrame(df[col])))

## One hot encoding
df = pd.get_dummies(df, columns=['adLP', 'groups'])

## Split the dataset into training and cross-validation
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.drop('adText',axis=1), df['adText'], test_size=0.1, random_state=101)

## Logistic Regression

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train,y_train)
pred_logreg = logreg.predict(X_test)
print ("lOGISTIC REGRESSION")
print ("confusion_matrix")
print(confusion_matrix(y_test, pred_logreg))
print ("Classification report")
print(classification_report(y_test, pred_logreg))
print ("accuracy score")
print(accuracy_score(y_test, pred_logreg))


from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
pred_gnb = gnb.predict(X_test)
print ("GaussianNB")
print ("confusion_matrix")
print(confusion_matrix(y_test, pred_gnb))
print("classification_report")
print(classification_report(y_test, pred_gnb))
print ("accuracy_score")
print(accuracy_score(y_test, pred_gnb))


from sklearn.svm import SVC
svc = SVC(gamma = 0.01, C = 100)#, probability=True)
svc.fit(X_train, y_train)
pred_svc = svc.predict(X_test)
print ("SVM")
print ("confusion_matrix")
print(confusion_matrix(y_test, pred_svc))
print("classification_report")
print(classification_report(y_test, pred_svc))
print ("accuracy_score")
print(accuracy_score(y_test, pred_svc))


from sklearn.neighbors import KNeighborsClassifier
KNC = KNeighborsClassifier(n_neighbors=3)
KNC.fit(X_train, y_train)
pred_KNC = KNC.predict(X_test)
print ("KNN")
print ("confusion_matrix")
print(confusion_matrix(y_test, pred_KNC))
print("classification_report")
print(classification_report(y_test, pred_KNC))
print ("accuracy_score")
print(accuracy_score(y_test, pred_KNC))


from sklearn import tree
d_tree = tree.DecisionTreeClassifier()
d_tree.fit(X_train, y_train)
pred_d_tree = d_tree.predict(X_test)
print ("Decision Tree")
print ("confusion_matrix")
print(confusion_matrix(y_test, pred_d_tree))
print("classification_report")
print(classification_report(y_test, pred_d_tree))
print ("accuracy_score")
print(accuracy_score(y_test, pred_d_tree))


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=50, max_depth=2,random_state=0)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
print ("Random Forest")
print ("confusion_matrix")
print(confusion_matrix(y_test, pred_rf))
print("classification_report")
print(classification_report(y_test, pred_rf))
print ("accuracy_score")
print(accuracy_score(y_test, pred_rf))