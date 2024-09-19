import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = (df['weight']/((df['height']/100) ** 2)).apply(lambda i: 1 if i > 25 else 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['gluc'] = df['gluc'].apply(lambda i: 0 if i == 1 else 1)

df['cholesterol'] = df['cholesterol'].apply(lambda i: 0 if i == 1 else 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    cat_plot = df.melt(id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    cat_plot = cat_plot.groupby(['cardio', 'variable', 'value']).value_counts().to_frame()
    cat_plot.rename(columns={0: 'total'}, inplace=True)
    cat_plot.reset_index(inplace=True)
    print(cat_plot.head())

    # Draw the catplot with 'sns.catplot()'
    plot = sns.catplot(x='variable', y='total', col='cardio', hue='value', kind='bar', data=cat_plot)
    fig = plot.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_2 = df[df['ap_lo'] <= df['ap_hi']]
    df_2 = df_2[df['height'] >= df['height'].quantile(0.025)]
    df_2 = df_2[df['height'] <= df['height'].quantile(0.975)]
    df_2 = df_2[df['weight'] >= df['weight'].quantile(0.025)]
    df_2 = df_2[df['weight'] <= df['weight'].quantile(0.975)]

    # Calculate the correlation matrix
    corr_matrix = df_2.corr()
    corr_matrix = corr_matrix.round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=np.bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=[11, 9])

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr_matrix, mask=mask, annot=True, cbar=True, square=True, fmt=".1f")

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
