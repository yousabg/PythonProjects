# -*- coding: utf-8 -*-
"""FinalProjectMcDonaldsCode.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IZx9Gg37NvLUyFHdyC1hQahXr6lJA0zP
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

#I begin by just doing some research on the dataset.
menu_df = pd.read_csv("https://raw.githubusercontent.com/yousabg/MostPopularNames/main/menu.csv", error_bad_lines=False)

menu_df.head()

menu_df["Item"].unique()

menu_df.columns

menu_df[menu_df['Item'] == 'Big Mac']

menu_df["Category"].unique()

plt.figure(figsize=(8, 6))
category_counts = menu_df['Category'].value_counts()
plt.bar(category_counts.index, category_counts.values, color='skyblue')
plt.xticks(rotation=45)
plt.title('Menu Item Categories')
plt.xlabel('Categories')
plt.ylabel('Count')
#Looking at how many items there are for each category

correlation_matrix = menu_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation In McDonalds Menu')
#Trying to see what variables are coorelated

plt.figure(figsize=(8, 6))
plt.scatter(menu_df['Calories'], menu_df['Saturated Fat'], color='purple', alpha=0.6)
plt.title('Calories vs Saturated Fat')
plt.xlabel('Calories')
plt.ylabel('Saturated Fat')
#Trying to visualize the coorelation between calories and saturated fats.

"""# Part 1 : Hypothesis Testing Using Change Model

We want to know if the Big Mac statistically has more calories than other menu items with a 5% significance level.

Null Hypothesis: Big Macs statistically have the same amount of calories as any other menu item

Alternative Hypothesis: Big Macs statistically have more calories than other menu items
"""

big_mac_calories = menu_df.loc[menu_df["Item"] == "Big Mac", 'Calories'].mean()
mean_calories = np.mean(menu_df['Calories'])
stan_dev_calories = np.std(menu_df['Calories'])
a = 0.05

from scipy.stats import norm as norm

random_variables = norm.rvs(loc=mean_calories, scale=stan_dev_calories, size=10000)


plt.figure(figsize=(8, 6))
plt.hist(random_variables, edgecolor='black', color='orange')
plt.title('Distribution of Calories in McDonald\'s Menu', color='orange')
plt.xlabel('Calories', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(big_mac_calories, color='yellow', linewidth=2, label='Calories in Big Mac')
plt.legend()
#Plotting the null hypothesis and the calories for the Big Mac on top to see how it compares to the null

p_value = np.sum(random_variables >= big_mac_calories) / len(random_variables)
p_value
#Finding the probability of geting a value as extreme or more than Big Mac calories.

"""# Part 2 : Permutation Test

We want to know if the average carbohydrates of Breakfast is *significantly* different than the average carbohydrates of other category items with a 5% significance level. We hypothesize that Breakfast has more carbs.

Null Hypothesis: The average carbohydrates of Breakfast are not significantly different from the average carbohydrates of other category items.

Alternative Hypothesis: The average carbohydrates of Breakfast are significantly higher than the average carbohydrates of other category items.
"""

breakfast_df = menu_df[menu_df["Category"] == "Breakfast"]
not_breakfast_df = menu_df[menu_df["Category"] != "Breakfast"]
average_breakfast_carbs = breakfast_df["Carbohydrates"].mean()
average_not_breakfast_carbs = not_breakfast_df["Carbohydrates"].mean()

obs_stat = abs(average_breakfast_carbs-average_not_breakfast_carbs)
obs_stat

not_breakfast_df['Category'] = 'Not Breakfast'
combined_df = not_breakfast_df.append(breakfast_df)
vals = combined_df["Category"].values
carbs = combined_df["Carbohydrates"].values

def simulate_test_stat(carbs, vals):
  categories_shuffled = vals
  np.random.shuffle(categories_shuffled)
  idx_breakfast = np.where(categories_shuffled == "Breakfast")
  avg_breakfast_carbs = np.average(carbs[idx_breakfast])
  idx_not_breakfast = np.where(categories_shuffled == "Not Breakfast")
  avg_not_breakfast_carbs= np.average(carbs[idx_not_breakfast])
  sim_test_stat = abs(avg_breakfast_carbs-avg_not_breakfast_carbs)
  return sim_test_stat
#Shuffling the categories (Breakfast and Not Breakfast) to conduct the permutation test.

simulate_test_stat(carbs, vals)

test_stats = []
for i in range(10000):
  test_stats.append(simulate_test_stat(carbs, vals))

plt.figure(figsize=(8, 6))
plt.hist(test_stats, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(obs_stat, color='red', linewidth=2, label='Observed Statistic of Averages')
plt.title('Simulated Test Statistics of Breakfast vs Non-Breakfast Carbs', color='skyblue')
plt.xlabel('Test Statistics', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
#Plotting the test statistics found and comparing it to the original statistic using the averages to see if there is a major variation in the two.

idx = np.where(test_stats > obs_stat)[0]
p_val = len(idx)/len(test_stats)
p_val
#Finding p-value, similar to part 1

"""# Part 3 : Bootstrapping a Confidence Interval

We want to estimate the mean amount of Saturated Fats in Beverages and Coffee & Tea
To do this we will bootstrap a 95% confidence interval.

Finally, we will ask if the mean amount of Saturated Fats in Desserts and Smoothies & Shakes falls inside the confidence region and is therefore similar to the amount of Saturated Fats in Beverages and Coffee & Tea

Null: The mean amount of Saturated Fats in Beverages is similar to the mean amount of Saturated Fats in Dessert.

Alternative: The mean amount of Saturated Fats in Beverages differs significantly from the mean amount of Saturated Fats in Dessert
"""

drinks_df = menu_df[(menu_df["Category"] == 'Coffee & Tea') | (menu_df["Category"] == 'Beverages')]
avg_drinks_sf = drinks_df["Saturated Fat"].mean()
avg_drinks_sf

def one_bootstrap_mean(sample_df):
  bootstrap_sample = sample_df.sample(n=len(sample_df), replace=True)
  bootstrapped_mean = bootstrap_sample["Saturated Fat"].mean()
  return bootstrapped_mean

one_bootstrap_mean(drinks_df)
#Function to find bootstrapped mean

means = []
for i in range(10000):
  means.append(one_bootstrap_mean(drinks_df))
left_interval_endpoint = np.percentile(means, 2.5)
print(left_interval_endpoint)

right_interval_endpoint = np.percentile(means, 97.5)
print(right_interval_endpoint)
#Finding left and right intervals of confidence interval.

interval = np.array([left_interval_endpoint, right_interval_endpoint])

desserts_df = menu_df[(menu_df["Category"] == 'Desserts') | (menu_df["Category"] == 'Smoothies & Shakes')]
avg_desserts_sf = desserts_df["Saturated Fat"].mean()


plt.figure(figsize=(8, 6))

plt.hist(means, color='darkgreen', edgecolor='black', alpha=0.7)
plt.axvline(avg_desserts_sf, c = 'r', label='Avg Saturated Fat in Desserts')
plt.plot(interval, [0, 0], linewidth = 20, c = 'lime')
plt.title('95% Bootstrapped Confidence Interval of Average Saturated Fats in Drinks', color='darkgreen')
plt.xlabel('Saturated Fats (g)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
#Plotting the null with the confidence interval, along with the average saturated fats in desserts to see if it falls within the confidence interval.

meansD = []
for i in range(10000):
  meansD.append(one_bootstrap_mean(desserts_df))

plt.figure(figsize=(8, 6))



plt.hist(means, alpha=0.7, label='Bootstrapped Means of Desserts', color='purple', edgecolor='black')
plt.hist(meansD, alpha=0.7, label='Bootstrapped Means of Beverages', color='orange', edgecolor='black')
plt.axvline(avg_desserts_sf, c = 'blue', label='Avg Saturated Fat in Desserts')
plt.axvline(avg_drinks_sf, c = 'red', label='Avg Saturated Fat in Drinks')
plt.title("Bootstrapped Means of Desserts and Drinks")
plt.xlabel("Saturated Fats (g)", fontsize = 12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
#Plotting the alternative to visualize the difference.