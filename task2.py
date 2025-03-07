# -*- coding: utf-8 -*-
"""Task2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ED8J3uzPtHaMx4Z2RrBkalyK6-l8g6Kd
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    file_path = '/content/Murad_Hossain_Dynamic_Process_Simulation_and_Bottleneck_Analysis.csv'

# Step 1: Data Import and Cleaning
def import_and_clean_data(file_path):
    # Load the data
    data = pd.read_csv(file_path)
    # Print the original columns for debugging
    print("Original Columns:", data.columns)
    # Instead of dropping rows, replace invalid values with 0 for 'Load' column if it exists
    if 'Load_Level' in data.columns:
        # Convert 'Load_Level' to numeric, errors='coerce' will handle non-numeric values
        data['Load_Level'] = pd.to_numeric(data['Load_Level'], errors='coerce')
        data['Load_Level'] = data['Load_Level'].fillna(0)  # Replace missing values with 0
        data['Load_Level'] = data['Load_Level'].clip(lower=0)  # Replace negative values with 0
    # Print the columns after cleaning
    print("Columns after cleaning:", data.columns)
    return data

# Step 2: Dynamic Load Analysis
def analyze_load(data):
    # Assuming 'Load_Level' and 'Task_Time' columns exist
    conditions = [
        (data['Load_Level'] <= 33),
        (data['Load_Level'] > 33) & (data['Load_Level'] <= 66),
        (data['Load_Level'] > 66)
    ]
    categories = ['Low', 'Medium', 'High']
    data['Load_Category'] = pd.cut(data['Load_Level'], bins=[-1, 33, 66, 100], labels=categories)

    # Average task efficiency by load category
    efficiency = data.groupby('Load_Category')['Task_Time (min)'].mean()

    # Tasks with the highest delays under peak load
    peak_load_tasks = data[data['Load_Category'] == 'High'].nlargest(5, 'Task_Time (min)')

    return efficiency, peak_load_tasks

# Step 3: Resource Bottleneck Detection
def detect_bottlenecks(data):
    # Calculate average and peak resource utilization
    avg_utilization = data.groupby('Task_Category')['Resource_Usage (%)'].mean()
    peak_utilization = data.groupby('Task_Category')['Resource_Usage (%)'].max()

    # Bottleneck detection
    bottlenecks = data.groupby('Task_Category')['Task_Time (min)'].max()

    return avg_utilization, peak_utilization, bottlenecks

# Step 4: Visualization
def create_visualizations(data, efficiency, bottlenecks):
    # Line chart for task completion times under different load conditions
    plt.figure(figsize=(10, 6))
    for category in data['Load_Category'].unique():
        subset = data[data['Load_Category'] == category]
        plt.plot(subset['Task_Time (min)'], label=category)  # Using 'Task_Time(min)'
    plt.legend()
    plt.title('Task Times by Load Category')
    plt.xlabel('Tasks')
    plt.ylabel('Time')
    plt.show()

    # Heatmap for resource usage intensity
    plt.figure(figsize=(10, 6))
    pivot_table = data.pivot_table(values='Resource_Usage (%)', index='Task_Category', columns='Load_Category', aggfunc='mean')
    sns.heatmap(pivot_table, annot=True, cmap='viridis')
    plt.title('Resource Usage Intensity')
    plt.show()

    # Bar chart for peak delays
    plt.figure(figsize=(10, 6))
    bottlenecks.sort_values().plot(kind='bar', color='orange')
    plt.title('Peak Delays by Task Category')
    plt.xlabel('Task Category')
    plt.ylabel('Peak Delay')
    plt.show()

# Main Function
def main():
    file_path = '/content/Murad_Hossain_Dynamic_Process_Simulation_and_Bottleneck_Analysis.csv'  # Replace with the path to your CSV file
    data = import_and_clean_data(file_path)
    efficiency, peak_load_tasks = analyze_load(data)
    avg_utilization, peak_utilization, bottlenecks = detect_bottlenecks(data)
    create_visualizations(data, efficiency, bottlenecks)

if __name__ == "__main__":
    main()