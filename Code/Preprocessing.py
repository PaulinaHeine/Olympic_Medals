
import numpy as np
import pandas as pd

def importation():
    # Import data
    summer = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/summer.csv")
    winter = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/winter.csv")
    dictionary = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/dictionary.csv")
    gdp = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/External/gdp.csv")
    return summer, winter, dictionary, gdp

# Checking for missing values
def missing_values():
    summer, winter, dictionary, gdp = importation()
    #summer.info()
    # 4 missing values in the Country Column;
    #summer[summer.isnull().any(axis=1)]
    #City = London -> Country = UK | We can fill the Country with United Kingdom (GBR)
    summer = summer.fillna("GBR")
    # No Nans left

    #winter.info()
    # 0 missing values
    #winter[winter.isnull().any(axis=1)]

    #dictionary.info()
    # at least 20 founded; GPD & Population
    #dictionary[dictionary.isnull().any(axis=1)]
    # Nans are ignored since we use external Data for GDP

    gdp = gdp.fillna(0)
    return summer, winter, dictionary, gdp

def concenate():
    summer, winter, dictionary,gdp = missing_values()
    # Adressing the concatenation into a new DataFrame called olympics;
    olympics = pd.concat([summer, winter], axis = 0, keys = ["Summer", "Winter"],
                        names = ["Edition"]).reset_index().drop(columns = "level_1")

    # Merging the recently created DataFrame olympics with the dictionary, assigning values for the ["Country"] column acording to their Country Code;
    olympics = olympics.merge(dictionary.iloc[:, :2], how='left', right_on="Code", left_on="Country").drop(columns=["Code"])
    # Renaming columns from the olympics DataFrame into appropriate labels
    olympics.rename(columns = {"Country_x": "Code", "Country_y": "Country_Name"}, inplace=True)
    # Check for Nans
    olympics[olympics.isnull().any(axis=1)]
    missing_index = olympics.loc[olympics.Country_Name.isnull()].index
    # olympics.loc[olympics.Country_Name.isnull()].Code.value_counts()

    # After checking the code for the countries that doesn't have a corresponding Countrie name, we save them into an object called missing_countries;
    missing_countries = olympics.loc[olympics.Country_Name.isnull()].Code.value_counts().index

    # Creating a pandas Series with the Country Codes as index and their respective values, the Country Names associated to them;
    # Source: https://en.wikipedia.org/wiki/List_of_IOC_country_codes
    mapping = pd.Series(index=missing_countries, name="Country", data = ["Soviet Union", "East Germany", "Romania", "West Germany", "Czechoslovakia",
                                   "Yugoslavia", "Unified Team", "Unified Team of Germany", "Mixed teams", "Serbia",
                                  "Australasia", "Russian Empire", "Montenegro", "Trinidad and Tobago", "Bohemia",
                                  "West Indies Federation", "Singapore", "Independent Olympic Participants"])

    # Assigning the Country names to each row, the missing index is passing the row labels, and "Code" the column,
    # and then we map the series created called Mapping;
    olympics.loc[missing_index, "Code"].map(mapping)

    # Add GDP
    olympics = olympics.merge(right=gdp, on='Code', how='left')


    # And now we fill the null values using the fillna and passing them directly into the DataFrame using inplace=True;
    olympics["Country_Name"].fillna(olympics.Code.map(mapping), inplace=True)
    summer = olympics[olympics["Edition"]=="Summer"]
    winter = olympics[olympics["Edition"]=="Winter"]

    olympics.fillna(0, inplace=True)


    ####find groupsorts
    #all participants of groupsports are listed
    groupsports_all = olympics.loc[olympics.duplicated(subset=["Year","City","Sport","Discipline","Event","Medal","Country_Name"], keep= False)]
    # only one representative is listed+individuals
    olympics_indandgroup = olympics.drop_duplicates(subset=["Year","City","Sport","Discipline","Event","Medal","Country_Name"],keep = "first")

    #### find individual sports
    individuals = olympics.drop_duplicates(subset=["Year","City","Sport","Discipline","Event","Medal","Country_Name"],keep = False)

    # only one representative per group
    groupsports_shrinked = groupsports_all.drop_duplicates(subset=["Year","City","Sport","Discipline","Event","Medal","Country_Name"],keep = "first")



    #olympics[olympics.isnull().any(axis=1)]
    # NO NANS LEFT
    return summer, winter, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup


def type_change():
    olympics = concenate()
    # MEDAL
    olympics.Medal = olympics.Medal.astype("category")
    olympics.Medal.cat.set_categories(["Bronze", "Silver", "Gold"], ordered=True)
    #olympics.info()
    return olympics

#olympics.to_csv('/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/olympics.csv', index=False)

def preprocessing():
    summer, winter, dictionary,gdp = missing_values()
    summer, winter, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup = concenate()
    return summer, winter, dictionary, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup



def preprocessing_clustering():
    summer, winter, dictionary, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup = preprocessing()

    # remove gdp from olympics_indandgroup (we don't need it for clustering)
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

    # remove countries and sports which do not exist anymore
    countries_remove = ["Soviet Union", "East Germany", "West Germany", "Czechoslovakia", 'Mixed teams',
                        "Yugoslavia", "Unified Team", "Unified Team of Germany", "Mixed teams"
                                                                                 "Australasia", "Russian Empire",
                        "Bohemia", 'Netherlands Antilles*'
                                   "West Indies Federation", "Independent Olympic Participants"]
    sports_remove = ['Basque Pelota', 'Cricket', 'Croquet', 'Tug of War', 'Lacrosse', 'Roque', 'Jeu de paume',
                     'Rackets', 'Water Motorsports', 'Polo']
    olympics_indandgroup = olympics_indandgroup[~olympics_indandgroup['Country_Name'].isin(countries_remove)]
    olympics_indandgroup = olympics_indandgroup[~olympics_indandgroup['Sport'].isin(sports_remove)]

    summer_indandgroup = olympics_indandgroup[olympics_indandgroup['Edition'] == 'Summer']
    winter_indandgroup = olympics_indandgroup[olympics_indandgroup['Edition'] == 'Winter']

    # if it is a winter sport, concatanate the word winter to the sport name
    olympics_indandgroup['Sport'] = np.where(olympics_indandgroup['Edition'] == 'Winter',
                                             olympics_indandgroup['Sport'] + ' Winter', olympics_indandgroup['Sport'])

    return summer, winter, dictionary, olympics, olympics_indandgroup, summer_indandgroup, winter_indandgroup







