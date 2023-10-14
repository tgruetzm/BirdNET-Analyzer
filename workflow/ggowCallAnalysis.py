import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates  # Import the mdates module

file_path = 'E:\BirdNet Audio 2023\GGOW Call Time Analysis\concatenated.2.txt'
# Define the column names for your DataFrame
column_names = ['Timestamp']
# Load the data from the text file into a DataFrame
df = pd.read_csv(file_path, header=None, names=column_names, delimiter='\t')


def showHeatmap():


    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y/%m/%d %H:%M:%S')

    df['hour'] = df['Timestamp'].dt.hour
    df['day'] = df['Timestamp'].dt.date

    print(df)

    # Create a pivot table to count calls for each hour of each day
    pivot_df = df.pivot_table(index='hour', columns='day', values='Timestamp', aggfunc='count')

    # Apply log transformation to the pivot table (for visualization)
    pivot_df_log = np.log1p(pivot_df)

    #@sns.set_style("whitegrid")
    # Create the heatmap with log-transformed data for visualization
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(pivot_df_log, cmap='YlGnBu', cbar=True, linewidths=1, linecolor='white')

    # Customize labels and title
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Hour of the Day', fontweight='bold')
    plt.title('GGOW Vocalization Heatmap', fontweight='bold')

    # Get the colorbar object
    cbar = ax.collections[0].colorbar

    # Create a new colorbar with original count values (exponentiate the values)
    cbar_labels = [str(int(np.exp(float(label.get_text())) - 1)) for label in cbar.ax.get_yticklabels()]
    cbar.ax.set_yticklabels(cbar_labels)
    cbar.set_label('Vocalization Count', fontweight='bold')

    # Show the plot
    plt.show()



def barGraphCallsByHour():

    # Convert 'Timestamp' to a datetime column if it's not already
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y/%m/%d %H:%M:%S')

    filtered = df[df['Timestamp'] <= '2023-05-01']
    # Extract the 'hour' component
    filtered['hour'] = filtered['Timestamp'].dt.hour

    

    # Group the data by hour and count the number of calls in each hour
    hourly_counts = filtered['hour'].value_counts().sort_index()

    # Create a bar graph
    plt.figure(figsize=(12, 6))
    plt.bar(hourly_counts.index, hourly_counts.values)

    # Customize labels and title
    plt.xlabel('Hour of the Day' , fontweight='bold')
    plt.ylabel('Number of Calls' , fontweight='bold')
    plt.title('Number of Calls by Hour through May 1st' , fontweight='bold')

    # Set the x-axis ticks to show all 24 hours
    plt.xticks(range(24))

    plt.grid(axis='y', linestyle='--', alpha=0.7)


    # Show the plot
    plt.show()


def barGraphCallsByDate():
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y/%m/%d %H:%M:%S')

    # Extract the 'date' component
    df['date'] = df['Timestamp'].dt.date

    # Group the data by date and count the number of calls for each date
    daily_counts = df['date'].value_counts().sort_index()

    # Create a bar graph
    plt.figure(figsize=(12, 6))
    plt.bar(daily_counts.index, daily_counts.values)

    # Customize labels and title
    plt.xlabel('Date' , fontweight='bold')
    plt.ylabel('Number of Calls' , fontweight='bold')
    plt.title('Number of Calls by Date' , fontweight='bold')

    # Show y-axis gridlines
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Specify the date format for the x-axis labels
    date_format = mdates.DateFormatter("%Y-%m-%d")

    # Set the x-axis major locator and formatter
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Set the interval to display every 7 days
    plt.gca().xaxis.set_major_formatter(date_format)

    plt.xlim(pd.Timestamp("2023-03-01"), daily_counts.index[-1])

    # Rotate x-axis labels for better readability (optional)
    plt.xticks(rotation=90)
    plt.show()



def areaPlot():
    sns.set_theme()
    # Load the data from the text file into a DataFrame
    file_path = 'E:\\BirdNet Audio 2023\\GGOW Call Time Analysis\\area-detection_date data2.txt'
    df = pd.read_csv(file_path, delimiter=',', names=['Area', 'Timestamp'])

    # Convert the 'Timestamp' column to datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

    # Group the data by 'Area' and 'Timestamp' and count the number of detections
    area_daily_counts = df.groupby(['Area', df['Timestamp'].dt.date]).size().reset_index(name='Count')


    # Create a line plot for each area
    plt.figure(figsize=(12, 6))
    sns.set_palette("bright")  # Set a color palette

    # Iterate through unique areas and plot each one
    for area in area_daily_counts['Area'].unique():
        area_data = area_daily_counts[area_daily_counts['Area'] == area]
        sns.lineplot(data=area_data, x='Timestamp', y='Count', label=area)
        plt.scatter(area_data['Timestamp'], area_data['Count'], s=10, marker='o', label='', color='black')

    # Customize labels and title
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Number of Detections', fontweight='bold')
    plt.title('Detections By Location', fontweight='bold')

    plt.xlim(pd.Timestamp("2023-03-01"), area_daily_counts['Timestamp'].max())
    plt.ylim(0)

    date_format = mdates.DateFormatter("%Y-%m-%d")
    # Set the x-axis major locator and formatter
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Set the interval to display every 7 days
    plt.gca().xaxis.set_major_formatter(date_format)
    # Rotate x-axis labels for better readability (optional)
    plt.xticks(rotation=90)

    # Show the legend
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Show the plot
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    plt.show()


if __name__ == '__main__':
    areaPlot()