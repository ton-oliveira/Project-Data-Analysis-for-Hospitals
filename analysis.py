import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Read CSV files with datasets
pd.set_option('display.max_columns', 8)
df_sport = pd.read_csv('test/sports.csv')
df_general = pd.read_csv('test/general.csv')
df_prenatal = pd.read_csv('test/prenatal.csv')

# Change the column names
df_prenatal = df_prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender', 'ultrasound': 'ultrasound'})
df_sport = df_sport.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'})

# Merge the data frames into one.
df_union = pd.concat([df_general, df_prenatal, df_sport], ignore_index=True)

# Delete the Unnamed: 0 column
df_union.drop(columns='Unnamed: 0', inplace=True)
# Delete all the empty rows
df_union.dropna(how='all', inplace=True)


# Correct all the gender column values
def prenatal_gender(row):
    if row.hospital == 'prenatal':
        row.gender = 'f'
    return row


df_union = df_union.apply(prenatal_gender, axis='columns')
df_union.gender.replace(to_replace=["male", 'man'], value='m', inplace=True)
df_union.gender.replace(to_replace=["female", 'woman'], value='f', inplace=True)

# Replace the NaN values in columns with zeros
values = {'bmi': 0, 'diagnosis': 0, 'blood_test': 0, 'ecg': 0, 'ultrasound': 0, 'mri': 0, 'xray': 0, 'children': 0,
          'months': 0}
df_union.fillna(value=values, inplace=True)

# Print random 20 rows of the resulting data frame
print(df_union.shape)
print(df_union.sample(n=20, random_state=30, ignore_index=False))

# The statistics
# 1) Which hospital has the highest number of patients?
print(df_union.groupby('hospital').hospital.count())
print('The answer to the 1st question is general')

# 2) What share of the patients in the general hospital suffers from stomach-related issues?
qtd_stomach = df_union.loc[(df_union.diagnosis == 'stomach') & (df_union.hospital == 'general')]
print('The answer to the 2nd question is', round((((qtd_stomach.shape[0] * 100) / 461) / 100), 3))

# 3) What share of the patients in the sports hospital suffers from dislocation-related issues?
print(df_union.groupby(['hospital', 'diagnosis']).diagnosis.size())
result_decimal = ((61 * 100) / 214) / 100
print('The answer to the 3rd question is', round(result_decimal, 3))

# 4) What is the difference in the median ages of the patients in the general and sports hospitals?
print(df_union.groupby('hospital').age.median())
print('The answer to the 4th question is', 19.0)

# 5) How many blood tests were taken?
print(df_union.groupby(['hospital', 'blood_test']).blood_test.count())
print('The answer to the 5th question is prenatal', 325, 'blood tests')


# Visualize it!
# 1) What is the most common age of a patient among all hospitals?
df_union.plot(y='age', kind='hist')
counts, bins = np.histogram(df_union.age, bins=range(0, 80, 15))
bins = 0.5 * (bins[:-1] + bins[1:])

fig, axs = plt.subplots(3, 1, figsize=(5, 15), sharex=True, sharey=True,
                        tight_layout=True)
axs[0].hist(df_union.age, bins=bins)
plt.show()

# 2) What is the most common diagnosis among patients in all hospitals?
df_union['diagnosis'].value_counts().plot(kind='pie')
df = df_union['diagnosis'].value_counts()
pie_diagnosis = px.pie(df, values='diagnosis', names=df.index)
pie_diagnosis.show()

fig1, ax1 = plt.subplots()
ax1.pie(df, labels=df.index, autopct='%1.1f%%')
ax1.axis('equal')
plt.show()

# 3) Build a violin plot of height distribution by hospitals
fig3 = px.violin(df_union, y='hospital', box=True, points='all',)
fig3.show()

data = df_union.groupby(['hospital']).diagnosis.value_counts()
fig2, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(9, 4), sharey=True)
ax1.set_title('Hospital Violin', fontsize=10)
ax1.set_ylabel('Observed values')
ax1.violinplot(data.values, showmeans=True, showmedians=True,
               showextrema=True)
plt.show()

print('The answer to the 1st question:', 15, '-', 35)
print('The answer to the 2nd question: pregnancy')
print("The answer to the 3rd question: It's because the sports hospital uses imperial units where the others use metric.")
