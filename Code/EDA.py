##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import plotly.express as px
import plotly.express as px
import plotly.io as pio
from seaborn import distplot

from Preprocessing import preprocessing
##
summer, winter, dictionary, olympics = preprocessing()

# Filter the top 10 countries
def t10_all():
    top10 = olympics['Country_Name'].value_counts().head(10).index

    # Filter data for the top 10 countries
    top10_data = olympics[olympics['Country_Name'].isin(top10)]

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
    plt.figure(figsize=(12, 8))
    ax = medal_counts_sorted.plot(kind='barh', stacked=True, color=[colors[col] for col in medal_counts_sorted.columns], figsize=(12, 8))

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
    return plt.show()


##
def plot_top_medals(olympics):
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

# how many "games were played" summer vs winter
# Set the default figure size for Seaborn plots
sns.set(rc={"figure.figsize": (6, 4)})
# Create a distribution plot
plot = sns.displot(winter["Year"], kde=True, color="orange")
# Add a title to the plot
plot.set(title="Distribution of Years in Winter Dataset")
#pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots.pdf'
#plot.savefig(pdf_filepath, format="pdf")

# Set the default figure size for Seaborn plots
sns.set(rc={"figure.figsize": (6, 4)})
# Create a distribution plot
plot = sns.displot(summer["Year"], kde=True, color="orange")
# Add a title to the plot
plot.set(title="Distribution of Years in Summer Dataset")
pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots/dist_summer.pdf'
plot.savefig(pdf_filepath, format="pdf")





####
#Men vs woman


# Assuming 'Year' is the column representing the years
# If not, replace 'Year' with the correct column name
gender_over_years = olympics.groupby(['Year', 'Gender']).size().unstack().reset_index()

# Create a complete set of years
all_years = pd.DataFrame({'Year': range(gender_over_years['Year'].min(), gender_over_years['Year'].max() + 1)})

# Merge with the existing data
gender_over_years = pd.merge(all_years, gender_over_years, on='Year', how='left').fillna(0)
#gender_over_years.set_index('Year', inplace=True)


sns.displot(gender_over_years, kde=True, color="orange")


pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots.pdf'
plot.savefig(pdf_filepath, format="pdf")

##
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
#Medal Distribution By Country
import plotly.graph_objs as go
from plotly.offline import plot

medals_map = olympics.groupby(['Country_Name', 'Code'])['Medal'].count().reset_index()

data = [dict(
    type='choropleth',
    autocolorscale=False,
    colorscale='Viridis',
    reversescale=True,
    showscale=True,
    locations=medals_map['Code'],
    z=medals_map['Medal'],
    locationmode='Code',
    text=medals_map['Country_Name'].unique(),
    marker=dict(
        line=dict(color='rgb(200,200,200)', width=0.5)),
    colorbar=dict(autotick=True, tickprefix='',
                  title='Medals')
)
]

layout = dict(
    title='Total Medals By Country',
    geo=dict(
        showframe=True,
        showocean=True,
        oceancolor='rgb(0,0,0)',
        projection=dict(
            type='Mercator',
        ),
    ),
)

fig = dict(data=data, layout=layout)

# Save the plot as an HTML file
plot(fig, validate=False, filename='worldmap2010.html')

### Plot for Summer vs Winter Olympics
medals_country_summer = summer.groupby(['Country_Name', 'Medal'])['Gender'].count().reset_index().sort_values(by='Gender', ascending=False)
medals_country_summer = medals_country_summer.pivot('Country_Name', 'Medal', 'Gender').fillna(0)
top_summer = medals_country_summer.sort_values(by='Gold', ascending=False)[:11]
# Create a new figure and subplot for Summer Olympics
fig, ax1 = plt.subplots(1, 2, figsize=(15, 6))
# Plot for Summer Olympics
top_summer.plot.barh(width=0.8, color=['#CD7F32', '#FFDF00', '#D3D3D3'], ax=ax1[0])
ax1[0].set_title('Medals Distribution Of Top 10 Countries (Summer Olympics)')
# Plot for Winter Olympics
medals_country_winter = winter.groupby(['Country_Name', 'Medal'])['Gender'].count().reset_index().sort_values(by='Gender', ascending=False)
medals_country_winter = medals_country_winter.pivot('Country_Name', 'Medal', 'Gender').fillna(0)
top_winter = medals_country_winter.sort_values(by='Gold', ascending=False)[:11]
# Plot for Winter Olympics
top_winter.plot.barh(width=0.8, color=['#CD7F32', '#FFDF00', '#D3D3D3'], ax=ax1[1])
ax1[1].set_title('Medals Distribution Of Top 10 Countries (Winter Olympics)')
# Adjust the layout
plt.tight_layout()
# Show the plots
plt.show()
pdf_filepath = '/Users/paulinaheine/PycharmProjects/Olympic_Medals/Plots'
plt.savefig(pdf_filepath)
##

