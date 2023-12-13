
import numpy as np
import pandas as pd

def importation():
    # Import data
    summer = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/summer.csv")
    winter = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/winter.csv")
    dictionary = pd.read_csv("/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/dictionary.csv")
    return summer, winter, dictionary

# Checking for missing values
def missing_values():
    summer, winter, dictionary = importation()
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
    return summer, winter, dictionary

def concenate():
    summer, winter, dictionary = missing_values()
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

    # And now we fill the null values using the fillna and passing them directly into the DataFrame using inplace=True;
    olympics["Country_Name"].fillna(olympics.Code.map(mapping), inplace=True)
    #olympics[olympics.isnull().any(axis=1)]
    ### NO NANS LEFT
    return olympics


def type_change():
    olympics = concenate()
    # MEDAL
    olympics.Medal = olympics.Medal.astype("category")
    olympics.Medal.cat.set_categories(["Bronze", "Silver", "Gold"], ordered=True)
    #olympics.info()
    return olympics

#olympics.to_csv('/Users/paulinaheine/PycharmProjects/Olympic_Medals/Data/Original/olympics.csv', index=False)

def preprocessing():
    summer, winter, dictionary = missing_values()
    olympics = concenate()
    return summer, winter, dictionary, olympics

def preprocessing_predict():
    summer, winter, dictionary = missing_values()
    olympics = type_change()
    return summer, winter, dictionary, olympics





