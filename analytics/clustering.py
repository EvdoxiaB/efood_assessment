import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import numpy as np

from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans


# import data in python
df = pd.read_csv(r'C:\Users\eudox\Desktop\pro\Efood\orders.csv')
print(df)

#Data manipulation for clustering
#Create frequency and order value measures
datamart=df.groupby(['user_id']).agg({
        'order_id': 'count',
        'amount': 'sum'
})

#Rename columns for easier interpretation
datamart.rename(columns= {'order_id': 'Frequency',
                          'amount': 'Order_val'}, inplace=True)

#Check the results
print(datamart)

#Statistics
print(datamart.describe())

#Plot the measures to examine the skew
sns.displot(datamart['Frequency'])
plt.show()

sns.displot(datamart['Order_val'])
plt.show()

#Unskew the data
datamart_log = np.log(datamart)
print(datamart_log)

sns.displot(datamart_log['Frequency'])
plt.show()
sns.displot(datamart_log['Order_val'])
plt.show()

#Normalize the variables
scaler = StandardScaler()
scaler.fit(datamart)

#Store for clustering
datamart_nor = scaler.transform(datamart)
print('mean: ', datamart_nor.mean(axis=0).round(2))
print('std: ',datamart_nor.std(axis=0).round(2))

#Clustering
#Decide the number of clusters using Elbow crieterion method
#Fit kmeans and calculate SSE
sse = {}
for k in range(1, 11):
	kmeans = KMeans(n_clusters = k, random_state = 1)
	kmeans.fit(datamart_nor)
	sse[k] = kmeans.inertia_ #sum of squared distances to closest cluster center

#Plot SSE for each k
plt.title('The Elbow Method')
plt.xlabel('k')
plt.ylabel('sse')
sns.pointplot(x=list(sse.keys()), y=list(sse.values()))
plt.show()

#Test the suitable number of clusters
#First k=3
kmeans = KMeans(n_clusters = 3, random_state = 1)

#Compute kmeans clustering
kmeans.fit(datamart_nor)

#Extract cluster labels from labels_attribute
cluster_labels = kmeans.labels_

#Analyze average measures for each cluster
#Create a cluster label column in the original dataset
datamart_k3 = datamart.assign(Cluster = cluster_labels)

#Calculate averages
datamart_cl3 = datamart_k3.groupby(['Cluster']).agg({
	'Frequency': 'mean',
	'Order_val': ['mean', 'count']
	}).round(0)

print(datamart_cl3)

#Same for k=4
kmeans = KMeans(n_clusters = 4, random_state = 1)

kmeans.fit(datamart_nor)

cluster_labels = kmeans.labels_

datamart_k4 = datamart.assign(Cluster = cluster_labels)

datamart_cl4 = datamart_k4.groupby(['Cluster']).agg({
	'Frequency': 'mean',
	'Order_val': ['mean', 'count']
	}).round(0)

print(datamart_cl4)

#Additional steps to evaluate difference between clusters
#Prepare data for snake plot
#Transform datamart_nor as DataFrame and add a Cluster column (k=3)
datamart_nor = pd.DataFrame(datamart_nor,
							index=datamart.index,
							columns=datamart.columns)

datamart_nor['Cluster'] = datamart_k3['Cluster']

datamart_melt_k3 = pd.melt(datamart_nor.reset_index(),
						id_vars=['user_id', 'Cluster'],
						value_vars=['Frequency', 'Order_val'],
						var_name='Attribute',
						value_name='Value')

# Visualize the snake plot
plt.title('Snake plot of standardized variables')
sns.lineplot(x="Attribute", y="Value", hue='Cluster', data=datamart_melt_k3)

# Relative importance of segment attributes (k = 3)
cluster_avg_k3 = datamart_k3.groupby(['Cluster']).mean()
population_avg = datamart.mean()
relative_imp_k3 = cluster_avg_k3 / population_avg - 1
print(relative_imp_k3.round(2))

# Plot heatmap
plt.figure(figsize=(8, 2))
plt.title('Relative importance of attributes')
sns.heatmap(data=relative_imp_k3, annot=True, fmt='.2f', cmap='RdYlGn')
plt.show()

#Same for k=4
datamart_nor = pd.DataFrame(datamart_nor,
							index=datamart.index,
							columns=datamart.columns)

datamart_nor['Cluster'] = datamart_k4['Cluster']

datamart_melt_k4 = pd.melt(datamart_nor.reset_index(),
						id_vars=['user_id', 'Cluster'],
						value_vars=['Frequency', 'Order_val'],
						var_name='Attribute',
						value_name='Value')

plt.title('Snake plot of standardized variables')
sns.lineplot(x="Attribute", y="Value", hue='Cluster', data=datamart_melt_k4)

cluster_avg_k4 = datamart_k4.groupby(['Cluster']).mean()
population_avg = datamart.mean()
relative_imp_k4 = cluster_avg_k4 / population_avg - 1
print(relative_imp_k4.round(2))

plt.figure(figsize=(8, 2))
plt.title('Relative importance of attributes')
sns.heatmap(data=relative_imp_k4, annot=True, fmt='.2f', cmap='RdYlGn')
plt.show()

#Export results in csv for creating personas
#Transform datamart_k3 and datamart_k4 as DataFrame
datamart_k3_df = pd.DataFrame(datamart_k3)
datamart_k3_df.to_csv(r'C:\Users\eudox\Desktop\pro\Efood\Cluster3.csv')

datamart_k4_df = pd.DataFrame(datamart_k4)
datamart_k4_df.to_csv(r'C:\Users\eudox\Desktop\pro\Efood\Cluster4.csv')
