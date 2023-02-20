# -*- coding: utf-8 -*-
"""Iris_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iqx2A5HxkIgVRGSTUFAqy0XBYVDj8L-_

# **Rajalakshmi Pillai**

# ***Iris Flower Classification***

---

# **Iris Dataset:**

The iris dataset contains measurements for **150 iris flowers** from three different species.The three classes of flowers, **Versicolor, Setosa, Virginica,**  and **50 samples** from each of three species of Iris and each class contains 4 features, ‘**Sepal length**’, ‘**Sepal width**’, ‘**Petal length**’, ‘**Petal width**’. 

 Four features were measured from each sample: the length and the width of the sepals and petals, in centimetres.

***The aim of the iris flower classification is to predict flowers based on their specific features.***

**The columns in this dataset are:**

Id

SepalLengthCm

SepalWidthCm

PetalLengthCm

PetalWidthCm

Species

**Import Libraries** 

Let us first start with the usual importing of relevant libraries which will be required for our analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

"""**Import the dataset**"""

data = pd.read_csv('/content/Iris.csv')

"""**The top 5 data**"""

data.head()

"""---


# **EDA- Explorartory Data Analysis**

**Count of how many instances (rows) and how many attributes 
(columns) the data contains with the shape property.**
"""

data.shape

"""**Overview of dataset**."""

data.info()

"""**Describing the dataset.**"""

data.describe()

"""**Checking for Null values**"""

data.isnull().sum()

"""There is no null values in our dataset.

**Check for Duplicate value**
"""

data.duplicated().sum()

"""There is no duplicate value.

**Analysing Target Feature - Species**

The number of instances (rows) that belong to each class.
"""

data.groupby('Species').size()

"""Types of Species - Setosa, Versicolor & Virginica

Each Species has 50 records

**Distribution of Features**

(Univariate Analysis)
"""

plt.figure(figsize=(15, 12))

plt.subplot(221) 
plt.hist(data['SepalLengthCm'],color = 'darkcyan')
plt.xlabel('Sepal Length in Cm')
plt.ylabel('Frequency')
plt.title('Distribution of Sepal Length')

plt.subplot(222) 
plt.hist(data['SepalWidthCm'],color = 'rosybrown')
plt.xlabel('Sepal Width in Cm')
plt.ylabel('Frequency')
plt.title('Distribution of Sepal Width')

plt.subplot(223) 
plt.hist(data['PetalLengthCm'],color = 'rosybrown')
plt.xlabel('Petal Length in Cm')
plt.ylabel('Frequency')
plt.title('Distribution of Petal Length')

plt.subplot(224) 
plt.hist(data['PetalWidthCm'],color = 'darkcyan')
plt.xlabel('Petal Width in Cm')
plt.ylabel('Frequency')
plt.title('Distribution of Petal Width')

plt.show()

"""**Sepal Width feature is Normally Distributed**

**Bivariate Analysis**
"""

plt.figure(figsize=(20,6))

colors = ['crimson','teal','purple']
species = ['Iris-virginica','Iris-versicolor', 'Iris-setosa']

plt.subplot(121) 

for i in range(3):
    x = data[data['Species'] == species[i]]
    plt.scatter(x['SepalLengthCm'],x['SepalWidthCm'],c=colors[i],label = species[i])
    
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Sepal Length & Sepal Width Trend W.R.T Species')
plt.legend()

plt.subplot(122) 

for i in range(3):
    x = data[data['Species'] == species[i]]
    plt.scatter(x['PetalLengthCm'],x['PetalWidthCm'],c=colors[i],label = species[i])
    
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.title('Petal Length & Petal Width Trend W.R.T Species')
plt.legend()

plt.show()

"""Sepal Length & Sepal Width have more overlappings whereas Petal Length & Petal Width have very few overlappings

**Co-relation Matrix**
"""

corr = data.corr()
fig,axis = plt.subplots(figsize = (8,4))
sns.heatmap(corr,annot = True, ax = axis,linewidths=.5,cmap="BuPu")

"""We Observe that the boxes with dark color are more corelated (Petal Width - Petal length) and the boxes with light color are less corelated.


---

# **Data Pre-processing**

NOTE: As we can see dataset contain six columns: Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm and Species. The actual features are described by columns 1-4. Last column contains labels of samples. Firstly we need to split data into two arrays: X (features) and y (labels).

# Dividing data into features and labels
"""

feature_cols= ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm','PetalWidthCm']
X = data[feature_cols].values
y = data['Species'].values

"""#K-Mean Clustering

Finding the optimal number of clusters for K-Means (Determining the value of K)
"""

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

x = data.iloc[:, [0, 1, 2, 3, 4]].values

wcss = []

for i in range(1,11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.figure(figsize = (12, 6))
plt.plot(range(1, 11), wcss, marker = '*',markersize='10',color='maroon',linestyle='dashed')
plt.title('Elbow Graph')
plt.xlabel('Number of Clusters')
plt.ylabel('Within Clusters Sum of Squares')
plt.show()

"""K = 1 to K = 2 (Steep Slope)

K = 2 to K = 3 (Gentle Slope)

K = 3 (Elbow Point)
"""

kmeans = KMeans(n_clusters = 3, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 42)
y_kmeans = kmeans.fit_predict(x)

plt.figure(figsize=(15,10))

plt.subplot(221) 
plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 1], s = 50, c = 'purple', label = 'Iris-setosa')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 1], s = 50, c = 'teal', label = 'Iris-versicolour')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 1], s = 50, c = 'crimson', label = 'Iris-virginica')
plt.xlabel('Id',size = 12)
plt.ylabel('Sepal Length',size = 12)
plt.title('Clustering Species W.R.T Sepal Length',size = 12)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], s = 100, c = 'yellow', label = 'Centroids')
plt.legend()

plt.subplot(222) 
plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 2], s = 50, c = 'purple', label = 'Iris-setosa')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 2], s = 50, c = 'teal', label = 'Iris-versicolour')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 2], s = 50, c = 'crimson', label = 'Iris-virginica')
plt.xlabel('Id',size = 12)
plt.ylabel('Sepal Width',size = 12)
plt.title('Clustering Species W.R.T Sepal Width',size = 12)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,2], s = 100, c = 'yellow', label = 'Centroids')
plt.legend()

plt.subplot(223) 
plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 3], s = 50, c = 'purple', label = 'Iris-setosa')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 3], s = 50, c = 'teal', label = 'Iris-versicolour')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 3], s = 50, c = 'crimson', label = 'Iris-virginica')
plt.xlabel('Id',size = 12)
plt.ylabel('Petal Length',size = 12)
plt.title('Clustering Species W.R.T Petal Length',size = 12)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,3], s = 100, c = 'yellow', label = 'Centroids')
plt.legend()

plt.subplot(224) 
plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 4], s = 50, c = 'purple', label = 'Iris-setosa')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 4], s = 50, c = 'teal', label = 'Iris-versicolour')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 4], s = 50, c = 'crimson', label = 'Iris-virginica')
plt.xlabel('Id',size = 12)
plt.ylabel('Petal Width',size = 12)
plt.title('Clustering Species W.R.T Petal Width',size = 12)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,4], s = 100, c = 'yellow', label = 'Centroids')
plt.legend()

plt.show()

"""After clustering We Observe that the clusters are perfectly seperated when the k = 3

# **Feature Selection**

Dropping Id because it has no use.
"""

df=data.drop(['Id'], axis=1)
df

"""#**Data Modeling**

**Importing relevent librarie's**
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix

"""**Splitting the data into train and test data**"""

x = df.drop("Species", axis=1)
y = df['Species']

x_train , x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

"""Lets see their shape"""

print('Shape of x_train:-',x_train.shape)

print('Shape of x_test:-',x_test.shape)

print('Shape of y_train:-',y_train.shape)

print('Shape of y_test:-',y_test.shape)

"""# **KNN > K-Nearest Neighbors**

# Training the model
"""

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(x_train, y_train)

"""# Testing the model

Predicting flower by giving new input
"""

new_x_Input = np.array([[6,2,4.3,2],[2, 2,1, 2],[4.3,2,4,1.3]])
new_x_pred = knn.predict(new_x_Input)
print("New Prediction: {}".format(new_x_pred))
print('')

"""# Accuracy Score (KNN)"""

print("Train Accuracy: ",round(knn.score(x_train, y_train)*100, 3))
print("Test Accuracy: ",round(knn.score(x_test, y_test)*100, 3))
print("")

"""

It looks like the model is predicting correctly because the setosa is shortest and virginica is the longest and versicolor is in between these two.
"""

plot_confusion_matrix(knn, x_train, y_train)
plot_confusion_matrix(knn, x_test, y_test)

plt.show()

"""# **Decision Tree**

# Importing relevent librarie's
"""

from sklearn.tree import DecisionTreeClassifier

"""# Training the model"""

dt = DecisionTreeClassifier(random_state = 42)
dt.fit(x_train, y_train)

"""# Testing the model

Predicting the Flower by giving new input
"""

new_x_Input = np.array([[3, 2,1.3, 3.2],[6,2,4.3,2],[4.3,2,4,1.3]])
new_x_pred = dt.predict(new_x_Input)
print("New Prediction: {}".format(new_x_pred))
print("")

"""It looks like the model is predicting correctly because the setosa is shortest and virginica is the longest and versicolor is in between these two.

# Accuracy Score
"""

print("Train Accuracy: ",round(dt.score(x_train, y_train)*100, 3))
print("Test Accuracy: ",round(dt.score(x_test, y_test)*100, 3))

plot_confusion_matrix(dt, x_train, y_train)
plot_confusion_matrix(dt, x_test, y_test)

plt.show()

"""from the above confusion matrix, we can easily interpret that there is no misclassification.

# **Conclusion**

1. K - Means Clustering performed well with k = 3.
2. Decision Tree Classifier performed best.
3. Our models are predecting correct flower spiceies after giving new measurements of features.

# Thank you
"""