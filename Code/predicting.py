import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
from Preprocessing import preprocessing
import pandas as pd
import sklearn
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


#TODO: cluster als feature einfügen+ mehr / confusionmatrix / Grafik mit träppchen

#Swap medal and country name

summer, winter, dictionary, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup = preprocessing()

medal_mapping = {'Gold': 3, 'Silver': 2, 'Bronze': 1}

# Apply the mapping to the 'Medal' column
olympics_indandgroup['Medal'] = olympics_indandgroup['Medal'].map(medal_mapping)


###clean up
countries_remove = ["Soviet Union", "East Germany", "West Germany", "Czechoslovakia", 'Mixed teams',
                        "Yugoslavia", "Unified Team", "Unified Team of Germany", "Mixed teams"
                                                                                 "Australasia", "Russian Empire",
                        "Bohemia", 'Netherlands Antilles*'
                                   "West Indies Federation", "Independent Olympic Participants"]
sports_remove = ['Basque Pelota', 'Cricket', 'Croquet', 'Tug of War', 'Lacrosse', 'Roque', 'Jeu de paume',
                     'Rackets', 'Water Motorsports', 'Polo']
olympics_indandgroup = olympics_indandgroup[~olympics_indandgroup['Country_Name'].isin(countries_remove)]
olympics_indandgroup = olympics_indandgroup[~olympics_indandgroup['Sport'].isin(sports_remove)]

#add gpd
gdp=[]
for i in range(len(olympics_indandgroup)):
    target_year = olympics_indandgroup["Year"].iloc[i]
    column_to_keep = f'{target_year}'
    if  target_year < 1960:
        gdp.append(0)
    elif target_year >= 1960:
        df = olympics_indandgroup[f'{target_year}']
        gdp.append(df.iloc[i])

olympics_indandgroup['gdp'] = np.array(gdp)

olympics_indandgroup = olympics_indandgroup.drop(columns=['Country Name', '1960',
                                                          '1961', '1962', '1963', '1964', '1965', '1966', '1967',
                                                          '1968', '1969',
                                                          '1970', '1971', '1972', '1973', '1974', '1975', '1976',
                                                          '1977', '1978',
                                                          '1979', '1980', '1981', '1982', '1983', '1984', '1985',
                                                          '1986', '1987',
                                                          '1988', '1989', '1990', '1991', '1992', '1993', '1994',
                                                          '1995', '1996',
                                                          '1997', '1998', '1999', '2000', '2001', '2002', '2003',
                                                          '2004', '2005',
                                                          '2006', '2007', '2008', '2009', '2010', '2011', '2012',
                                                          '2013', '2014',
                                                          '2015', '2016', '2017', '2018', '2019', '2020',
                                                          'Unnamed: 65'])


olympics_indandgroup_2 = olympics_indandgroup

#Target encoding Athlete
df = olympics_indandgroup.groupby(["Athlete"]).mean()['Medal'].reset_index()
olympics_indandgroup = pd.merge(olympics_indandgroup, df, on=["Athlete"], how='left')
olympics_indandgroup = olympics_indandgroup.rename(columns={"Medal_x":"Medal",'Medal_y': 'Target_athlete'})
olympics_indandgroup["Medal"]. corr(olympics_indandgroup["Target_athlete"])
#0.8790464313875114 -> Take in model

# Target encoding
# Group by the specified columns and calculate the mean of the 'Medal' columnCh
df = olympics_indandgroup.groupby(['Country_Name', 'Discipline',"Sport","Event","Gender"]).mean()['Medal'].reset_index()
# Merge the resulting DataFrame with the original 'olympics' DataFrame
olympics_indandgroup = pd.merge(olympics_indandgroup, df, on=['Country_Name', 'Discipline',"Sport","Event","Gender"], how='left')
olympics_indandgroup = olympics_indandgroup.rename(columns={"Medal_x":"Medal",'Medal_y': 'Target_CDSEG'})
olympics_indandgroup["Medal"]. corr(olympics_indandgroup["Target_CDSEG"])
#0.6726422369504637 ->Take in  model


# Edition
df = olympics_indandgroup.groupby(['Country_Name', 'Discipline',"Sport","Event","Edition"]).mean()['Medal'].reset_index()
# Merge the resulting DataFrame with the original 'olympics' DataFrame
olympics_indandgroup = pd.merge(olympics_indandgroup, df, on=['Country_Name', 'Discipline',"Sport","Event","Edition"], how='left')
olympics_indandgroup = olympics_indandgroup.rename(columns={"Medal_x":"Medal",'Medal_y': 'Target_CDSEE'})
olympics_indandgroup["Medal"]. corr(olympics_indandgroup["Target_CDSEE"])
# 0.6386844825291602 ->Take in Model


# Country Name
df = olympics_indandgroup.groupby(['Country_Name']).mean()['Medal'].reset_index()
# Merge the resulting DataFrame with the original 'olympics' DataFrame
olympics_indandgroup = pd.merge(olympics_indandgroup, df, on=['Country_Name'], how='left')
olympics_indandgroup = olympics_indandgroup.rename(columns={"Medal_x":"Medal",'Medal_y': 'Target_Country'})
olympics_indandgroup["Medal"]. corr(olympics_indandgroup["Target_Country"])
# 0.6386844825291602 ->Take in Model


olympics_indandgroup = olympics_indandgroup.drop(['Edition', 'City', 'Sport', 'Discipline', 'Athlete', 'Code',
       'Gender', 'Event', 'Country_Name'],axis=1)


#predict the outcomes of the 2014 olympics
train =olympics_indandgroup[olympics_indandgroup["Year"]!=2014]
test = olympics_indandgroup[olympics_indandgroup["Year"]==2014]

X_train = train.drop(["Medal"],axis=1)
X_test = test.drop(["Medal"],axis=1)

y_train = train.Medal.astype('category')
y_test = test.Medal.astype('category')

'''
Normal prediction
X = olympics_indandgroup.drop(["Medal"],axis=1)

y = olympics_indandgroup.Medal.astype('category')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
'''


#insert the best values
gbc = GradientBoostingClassifier()

gbc = gbc.fit (X_test, y_test)
#gbc.predict_proba()
y_pred = gbc.predict(X_test)
print(gbc.score(X_test, y_test))

for fn, fi in sorted(zip(X.columns, gbc.feature_importances_), key=lambda xx: xx[1], reverse=True):
  print(f"{fn}: {fi:.3f}")


# Now test on last two olympics
cm = sklearn.metrics.confusion_matrix(y_test,y_pred)

# For 2014 winter prediction
new = olympics_indandgroup_2.iloc[14145:]
new["prediction"] = y_pred
#2014 actuals
trues = olympics_indandgroup_2.iloc[14145:]

def plot():
    sns.set(style="darkgrid")
    top10 = trues['Country_Name'].value_counts().head(10).index
    # Filter data for the top 10 countries
    top10_data = trues[trues['Country_Name'].isin(top10)]
    # Create a DataFrame with the count of medals for each country
    medal_counts = (
        top10_data.groupby(['Country_Name', 'Medal'])
        .size()
        .unstack(fill_value=0)

    )
    # Calculate the total number of medals for each country
    medals = medal_counts.sum(axis=1)
    # Sort the DataFrame by the total number of medals in descending order
    medals = medals.sort_values(ascending=True)
    # Define explicit colors for Gold, Silver, and Bronze

    # Create a horizontal stacked bar plot with explicit colors
    plt.title("Predicted top 10 Countries by total Number of Medals in 2014", fontsize=18)
    plt.xlabel("Number of Medals", fontsize=15)
    return medals.plot(kind='barh')

    # Invert the y-axis for better readability