
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


from Preprocessing import preprocessing

##
summer, winter, dictionary, olympics, groupsports_all, groupsports_shrinked, individuals, olympics_indandgroup = preprocessing()

# Filter the top 10 countries in winning medals
def t10_all():
    # Set seaborn style with a grey background
    sns.set(style="darkgrid")
    top10 = olympics_indandgroup['Country_Name'].value_counts().head(10).index
    # Filter data for the top 10 countries
    top10_data = olympics_indandgroup[olympics_indandgroup['Country_Name'].isin(top10)]
    # Create a DataFrame with the count of medals for each country
    medal_counts = (
        top10_data.groupby(['Country_Name', 'Medal'])
        .size()
        .unstack(fill_value=0)
        [['Bronze', 'Silver', 'Gold']]  # Ensure the correct order of columns
    )
    # Calculate the total number of medals for each country
    medal_counts['Total'] = medal_counts.sum(axis=1)
    # Sort the DataFrame by the total number of medals in descending order
    medal_counts_sorted = medal_counts.sort_values(by='Total', ascending=False).drop('Total', axis=1)
    # Define explicit colors for Gold, Silver, and Bronze
    colors = {'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'peru'}
    # Create a horizontal stacked bar plot with explicit colors
    plt.figure(figsize=(15, 15))
    ax = medal_counts_sorted.plot(kind='barh', stacked=True, color=[colors[col] for col in medal_counts_sorted.columns],
                                  width=0.8)
    # Replace specific country labels
    country_labels = {'United States': 'USA', 'Soviet Union': 'UdSSR', 'United Kingdom': 'UK'}
    tick_positions = range(len(top10))
    plt.yticks(tick_positions, [country_labels.get(country, country) for country in top10])
    # Add labels and title
    plt.title("Top 10 Countries by Total Number of Medals", fontsize=18)
    plt.xlabel("Number of Medals", fontsize=15)
    plt.ylabel("Country", fontsize=15)
    # Invert the y-axis for better readability
    plt.gca().invert_yaxis()
    # Display the legend at the bottom right inside the box
    plt.legend(title='Medal', bbox_to_anchor=(1, 0), loc='lower right', fontsize=12)
    # Add text annotations for each part of the bars
    for i, country in enumerate(top10):
        total = 0
        for medal_type in ['Bronze', 'Silver', 'Gold']:
            count = medal_counts.loc[country, medal_type]
            if count > 0:
                plt.text(total + count / 2, i, f"{int(count)}", ha='center', va='center', fontsize=10, color='black')
                total += count
    # Display the plot
    pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots/1.pdf'
    plt.savefig(pdf_filepath, format="pdf")
    return plt.show()
#t10_all()



##
def plot_top_medals(olympics_indandgroup):
    # Function to create a bar plot with medal counts and labels
    def plot_medals(medal_type, medal_counts, ax):
        colors = {'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'peru'}
        counts = medal_counts[medal_counts['Medal'] == medal_type].groupby('Country_Name').size().sort_values(ascending=False).head(10)

        bars = counts.plot(kind='barh', color=[colors[medal_type]], ax=ax)

        for bar in bars.patches:
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}',
                    va='center', fontsize=12, color='black')

        ax.set_title(f"Top 10 Countries - {medal_type} Medals", fontsize=16)
        ax.set_xlabel("Number of Medals", fontsize=12)
        ax.set_ylabel("Country", fontsize=12)
        ax.invert_yaxis()  # Invert y-axis for better readability
        ax.legend([medal_type], loc='lower right', fontsize=10)

    # Create a combined figure with subplots for Gold, Silver, and Bronze
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot Gold Medals
    plot_medals('Gold', olympics, axes[0])

    # Plot Silver Medals
    plot_medals('Silver', olympics, axes[1])

    # Plot Bronze Medals
    plot_medals('Bronze', olympics, axes[2])

    # Adjust layout without tight_layout
    plt.tight_layout()

    # Display the plot
    plot = plt.show()

    return plot
##

# how many "games were played"
# Set the default figure size for Seaborn plots


# Set the default figure size for Seaborn plots
sns.set(rc={"figure.figsize": (5, 5)})
# Create a distribution plot
plot = sns.displot(olympics_indandgroup["Year"], kde=True, color="orange")
# Add a title to the plot
plot.set(title="Distribution of Medals 1869-2014",fontsize=18)
pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots/dist_medals.pdf'
plot.savefig(pdf_filepath, format="pdf")





####
#Men vs woman

# NOW ALL AVAILABLE DATA IS USED SINCE IT DOES NOT MATTER IF IT IS A TEAM!!!
# Assuming 'Year' is the column representing the years
# If not, replace 'Year' with the correct column name

import matplotlib.pyplot as plt


# Group by Year and Gender and calculate the size
grouped_data = olympics.groupby(['Year', 'Gender']).size().unstack(level=1)
#grouped_summer = summer.groupby(["Year","Gender"]).Medal.count().reset_index().pivot("Year","Gender","Medal").fillna(0)
# Create a figure and axis
fig, ax = plt.subplots(figsize=(15, 15))


# Plot the stacked bar chart
grouped_data.plot(kind='bar', stacked=True, color=['blue', 'red'], ax=ax)
#grouped_summer.plot(kind="line")


# Set title and labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
plt.title('Male vs. Female Participation', fontsize=18)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Count', fontsize=14)


# Add legend
plt.legend(['Male', 'Female'],fontsize=12)
pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots/malevsfemale.pdf'
plt.savefig(pdf_filepath, format="pdf")

# Show the plot
plt.show()





## Gdp over years vs Medals over years


#only 2014
y = list(range(1988, 2001, 4))
for year in y:
    # Filter the DataFrame for the specified years
    filtered_df = olympics_indandgroup[olympics_indandgroup['Year']==year]

    #only gdp of 2014
    g14 = filtered_df[['Country_Name',str(year)]
    ].drop_duplicates(keep="first")
    #medalcountt of 2014
    y2014 = filtered_df.groupby(["Year","Country_Name"])["Medal"].count().to_frame()

    eda_gdp = y2014.merge(g14, how='left', right_on="Country_Name", left_on="Country_Name")




    # Specify the columns to normalize
    columns_to_normalize = [str(year)]


    # Normalize the specified columns
    scaler = MinMaxScaler()
    eda_gdp[columns_to_normalize] = scaler.fit_transform(eda_gdp[columns_to_normalize])



    # Scatter plot
    for year in columns_to_normalize:
        plt.scatter(eda_gdp[year], eda_gdp['Medal'], label=year,alpha= 0.69)
    sns.set(style="darkgrid")
    # Adding labels and title
    plt.xlabel('GDP per Capita (normalized)',fontsize=14)
    plt.ylabel('Medal',fontsize=14)
    plt.title('Scatter Plot of Medals vs. GDP', fontsize=20)



    # Adding a legend
    plt.legend()

    # Show the plot
    plt.show()

