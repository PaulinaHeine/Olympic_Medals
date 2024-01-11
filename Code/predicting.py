from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
from Preprocessing import preprocessing
import pandas as pd
import sklearn


# Edition nicht so (2.003/2.0003)


summer, winter, dictionary, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup = preprocessing()

medal_mapping = {'Gold': 3, 'Silver': 2, 'Bronze': 1}

# Apply the mapping to the 'Medal' column
olympics_indandgroup['Medal'] = olympics_indandgroup['Medal'].map(medal_mapping)


# Group by the specified columns and calculate the mean of the 'Medal' column
df = olympics_indandgroup.groupby(['Country_Name', 'Discipline',"Sport","Event","Gender"]).mean()['Medal'].reset_index()
# Merge the resulting DataFrame with the original 'olympics' DataFrame
olympics_indandgroup = pd.merge(olympics_indandgroup, df, on=['Country_Name', 'Discipline',"Sport","Event","Gender"], how='left')



#edition_dummies = pd.get_dummies(olympics_indandgroup['Edition'], prefix='Edition')
# Concatenate the one-hot encoded columns to the original DataFrame
#olympics_indandgroup = pd.concat([olympics_indandgroup, edition_dummies], axis=1)

#edition_dummies = pd.get_dummies(olympics_indandgroup['Country_Name'], prefix='Edition')
# Concatenate the one-hot encoded columns to the original DataFrame
#olympics_indandgroup = pd.concat([olympics_indandgroup, edition_dummies], axis=1)


#edition_dummies = pd.get_dummies(olympics_indandgroup['Sport'], prefix='Edition')
# Concatenate the one-hot encoded columns to the original DataFrame
#olympics_indandgroup = pd.concat([olympics_indandgroup, edition_dummies], axis=1)

#edition_dummies = pd.get_dummies(olympics_indandgroup['Discipline'], prefix='Edition')
# Concatenate the one-hot encoded columns to the original DataFrame
#olympics_indandgroup = pd.concat([olympics_indandgroup, edition_dummies], axis=1)

#edition_dummies = pd.get_dummies(olympics_indandgroup['Event'], prefix='Edition')
# Concatenate the one-hot encoded columns to the original DataFrame
#olympics_indandgroup = pd.concat([olympics_indandgroup, edition_dummies], axis=1)


edition_dummies = pd.get_dummies(olympics_indandgroup['Gender'], prefix='Edition')
# Concatenate the one-hot encoded columns to the original DataFrame
olympics_indandgroup = pd.concat([olympics_indandgroup, edition_dummies], axis=1)



olympics_indandgroup = olympics_indandgroup.drop(['Edition', 'City', 'Sport', 'Discipline', 'Athlete', 'Code',
       'Gender', 'Event', 'Country_Name',"Country Name",'Unnamed: 65'],axis=1)


X = olympics_indandgroup.drop(["Medal_x"],axis=1)

y = olympics_indandgroup.Medal_x.astype('category')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)




#insert the best values
gbc = GradientBoostingClassifier()

gbc = gbc.fit (X_test, y_test)

print(gbc.score(X_test, y_test))