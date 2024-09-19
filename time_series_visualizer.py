import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date', parse_dates=True)

# Clean data
df = df[(df['value'] >= df.value.quantile(.025)) & (df['value'] <= df.value.quantile(.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(32, 10))
    ax.plot(df.index, df.value)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=25)
    ax.set_xlabel('Date', fontsize=20)
    ax.set_ylabel('Page Views', fontsize=20)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    plot = df_bar.plot.bar(figsize=(15.14, 13.3))
    plot.legend(months, title='Months', prop={'size': 20})
    plot.set_xlabel('Years', fontsize=20)
    plot.set_ylabel('Average Page Views', fontsize=20)
    fig = plot.figure


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['sorted_months'] = df_box['date'].dt.month
    df_box = df_box.sort_values('sorted_months')

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(figsize=(28.8, 10.8), ncols=2)
    sns.boxplot(x=df_box.year, y=df_box.value, ax=ax[0]).set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views')
    sns.boxplot(x=df_box.month, y=df_box.value, ax=ax[1]).set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
