#fb_ads
The dataset was downloaded from [here](https://github.com/kyiyeunggoh/kyiyeunggoh.github.io/blob/master/Other%20Projects/Russian%20FB%20Ads/all_fb_ads.xlsx). “all_fb_ads” is a dataset published by the US Government, containing a sample selection of advertisements sponsored by the Russian Government in an attempt to influence the 2016 US elections. The fields in this dataset are defined below:
1. AdID: The ID# of the advertisement
2. adText: The text contained within the ad
3. adSpend: The dollar value spent on promoting/distributing that ad
4. adLP: the URL associated with the ad
5. adImpress: The number of ad impressions made
6. adClicks: The number of times the ad was clicked
7. adCreation: The date and time the ad was created
8. groups: The targeted audience for the ad
9. adLocation: The location(s) in which the ad was released
10. adStates: The state(s) in which the ad was released
11. adDate: See adCreation

When checked for number null values in each column, we get the following values:
adID                                 0
adText                              26
adSpend 0
adLP 28
adImpress 78
adClicks 70
adCreation 1
groups 186
adLocation_cleaned  2664
adStates 2683
adDate 91


It can be seen that adLocation and adState are extremely sparse columns and hence doesn’t have much impact on the dependent value. Which is why I did not want it to take a lot of space but still wanted it to have some significance. Which is why I just took the states to consideration. I split adState up to list of states and used one-hot-encoding. The frequency of ad in each state is shown below.

![](https://github.com/sumanp31/fb_ads/blob/master/plots/State.png) 

I filled null values in adText with “No Text”. Later, after a quick view of read through the uniques values in adText, I came up with a set of words that suggests that the ad was about the 2016 presidental election. The set of words is as follow: [‘Trump' , 'wall' , 'war' , 'politics' , 'racism' , 'Clinton' , 'liberty', 'rally' , 'election' , 'president' , 'ISIS' ,'Syria' , 'terror']. If these words are present in the adText then it is denoted as 1 or as 0. This is later used as the dependent variable. The idea behind this decision is that we are trying to figure out why which of the ads are capable of manipulating the election result.


For adLP, any entry that isn’t an url is replaced by none. And I cleaned it down to the website name intead of the page details.
"Stat for all the ads"
![ ](https://github.com/sumanp31/fb_ads/blob/master/plots/adLP1.png )
 "Stat for the ads with political agenda"
![ ](https://github.com/sumanp31/fb_ads/blob/master/plots/adLP2.png )

Fill null values of adClick by 0 and null value of adImpress by the corresponding adClick. This is because, ad Impression is the number of times an ad was called from it’s cource, irrespective of whether it was clicked by the user. So it has to be at greater than equal to the number of times it was clicked.
"adClick for all the ads"
![ ](https://github.com/sumanp31/fb_ads/blob/master/plots/adClick1.png )
"adClick for the ads with political agenda"
![ ](https://github.com/sumanp31/fb_ads/blob/master/plots/adClick2.png )
 "adImpress for all the ads"
![ ](https://github.com/sumanp31/fb_ads/blob/master/plots/adImpress1.png )
"adImpress for the ads with political agenda"
![ ](https://github.com/sumanp31/fb_ads/blob/master/plots/adImpress2.png )

I separated out the dates and times from the adCreation. Converted the date to number of days before the date of election “11/08/16”. I also converted any non-datetime value to “01/01/11” that is, a day before the previous election and any ad before that shouldn’t effect the 2016 election. Converted time to 24 hr format and just considered the hour and droped the minute and second.

This cleaned dataframe is saved as “cleaned_all_fb_ads.csv”
Given that the number of training example is small, I divided the dataset into training and cross-validation set at a ratio of 80%-20%. Numerical data are normalised using sklearn.MinMaxScaler() and categorical data are encoded using one-hot-encoding pandas.get_dummies(). When fit to
Logistic Regression, I got the following evaluation matrics: