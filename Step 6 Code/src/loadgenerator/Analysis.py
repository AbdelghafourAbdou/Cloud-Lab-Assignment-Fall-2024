import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import strftime, localtime

# load CSVs
statsDf = pd.read_csv('./CSVs/loadgenerator_stats.csv')
statsHistoryDf = pd.read_csv('./CSVs/loadgenerator_stats_history.csv')

timeStatsDf = statsDf.groupby(['Type', 'Name']).mean()
requestsDf = statsDf.groupby(['Type', 'Name']).sum().reset_index()

# response time analysis
print("Average Response Time:", timeStatsDf['Average Response Time'].mean(), "ms")
print("Total Average Response Time:", statsHistoryDf['Total Average Response Time'].mean(), "ms")
print("90th Percentile:", timeStatsDf['Average Response Time'].quantile(0.9), "ms")
print("Max Response Time:", statsHistoryDf['Total Max Response Time'].max(), "ms")
print("Min Response Time:", statsHistoryDf.loc[statsHistoryDf['Total Min Response Time'] != 0, 'Total Min Response Time'].min(), "ms")
print("Max Requests/s:", statsHistoryDf.groupby('Timestamp').sum()['Requests/s'].max(),  'requests/s')
print("The total average content size generated:", (statsHistoryDf['Total Average Content Size'].sum()) / 1000000, 'MB')

# plot the response time distribution
timeStatsDf['Average Response Time'].plot(kind='hist', bins=50, color='skyblue', edgecolor='black')
plt.title('Response Time Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Response Time (ms)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# preparing the data
endpoints = requestsDf["Name"].unique()

getRequestCount = requestsDf[requestsDf["Type"] == "GET"].set_index("Name").reindex(endpoints, fill_value=0)
postRequestCount = requestsDf[requestsDf["Type"] == "POST"].set_index("Name").reindex(endpoints, fill_value=0)

getRequestsPerSecond = requestsDf[requestsDf["Type"] == "GET"].set_index("Name")["Requests/s"].reindex(endpoints, fill_value=0)
postRequestsPerSecond = requestsDf[requestsDf["Type"] == "POST"].set_index("Name")["Requests/s"].reindex(endpoints, fill_value=0)

getFailuresPerSecond = requestsDf[requestsDf["Type"] == "GET"].set_index("Name")["Failures/s"].reindex(endpoints, fill_value=0)
postFailuresPerSecond = requestsDf[requestsDf["Type"] == "POST"].set_index("Name")["Failures/s"].reindex(endpoints, fill_value=0)

x = np.arange(len(endpoints))
width = 0.4

# plotting Request Count by Type and Endpoint Name
plt.figure(figsize=(12, 6))
plt.bar(x - width / 2, getRequestCount["Request Count"], width, label="GET", color="skyblue", edgecolor="black")
plt.bar(x + width / 2, postRequestCount["Request Count"], width, label="POST", color="orange", edgecolor="black")
plt.title("Requests Count by Endpoint and Type", fontsize=16, fontweight="bold")
plt.xlabel("Endpoint", fontsize=14)
plt.ylabel("Request Count", fontsize=14)
plt.xticks(x, endpoints, rotation=45, ha="right")
plt.legend(title="Request Type", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# plotting Requests/s by Type and Endpoint Name
plt.bar(x - width / 2, getRequestsPerSecond, width, label="GET", color="skyblue", edgecolor="black")
plt.bar(x + width / 2, postRequestsPerSecond, width, label="POST", color="orange", edgecolor="black")
plt.title("Requests/s by Endpoint and Type", fontsize=16, fontweight="bold")
plt.xlabel("Endpoint", fontsize=14)
plt.ylabel("Requests/s", fontsize=14)
plt.xticks(x, endpoints, rotation=45, ha="right")
plt.legend(title="Request Type", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# plotting Failures/s by Type and Endpoint Name
plt.bar(x - width / 2, getFailuresPerSecond, width, label="GET", color="skyblue", edgecolor="black")
plt.bar(x + width / 2, postFailuresPerSecond, width, label="POST", color="orange", edgecolor="black")
plt.title("Failures/s by Endpoint and Type", fontsize=16, fontweight="bold")
plt.xlabel("Endpoint", fontsize=14)
plt.ylabel("Failures/s", fontsize=14)
plt.xticks(x, endpoints, rotation=45, ha="right")
plt.legend(title="Request Type", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# preparing the data
statsHistoryByTimeDf = statsHistoryDf.groupby('Timestamp').sum()['Total Request Count']
statsHistoryByTimeDf = statsHistoryByTimeDf.reset_index()
# convert Epoch Timestamp to readable time
statsHistoryByTimeDf['Timestamp'] = statsHistoryByTimeDf['Timestamp'].apply(
    lambda x: strftime('%H:%M:%S', localtime(x))
)

# plot Total Request Count Over Time
plt.plot(statsHistoryByTimeDf['Timestamp'], statsHistoryByTimeDf['Total Request Count'], marker='o', color='#003B6F', label="Total Request Count")
plt.title("Total Request Count Over Time", fontsize=16, fontweight="bold")
plt.xlabel("Timestamp", fontsize=14)
plt.ylabel("Total Request Count", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.legend()
plt.show()

# preparing the data
statsHistoryByTimeDf = statsHistoryDf.groupby('Timestamp').sum()['User Count']
statsHistoryByTimeDf = statsHistoryByTimeDf.reset_index()
# convert Epoch Timestamp to readable time
statsHistoryByTimeDf['Timestamp'] = statsHistoryByTimeDf['Timestamp'].apply(
    lambda x: strftime('%H:%M:%S', localtime(x))
)

# plot User Count Over Time
plt.plot(statsHistoryByTimeDf['Timestamp'], statsHistoryByTimeDf['User Count'], marker='o', color='#003B6F', label="User Count")
plt.title("User Count Over Time", fontsize=16, fontweight="bold")
plt.xlabel("Timestamp", fontsize=14)
plt.ylabel("User Count", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.legend()
plt.show()
