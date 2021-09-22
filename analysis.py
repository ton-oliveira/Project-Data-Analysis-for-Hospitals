import pandas as pd


pd.set_option('display.max_columns', 8)
# Read CSV files with datasets
df_general = pd.read_csv('test/general.csv')
df_prenatal = pd.read_csv('test/prenatal.csv')
df_sport = pd.read_csv('test/sports.csv')

# Change the column names
df_prenatal = df_prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender', 'ultrasound': 'ultrasound'})
df_sport = df_sport.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'})

# Merge the data frames into one.
df_union = pd.concat([df_general, df_prenatal, df_sport], ignore_index=True)
# Delete the Unnamed: 0 column
df_union.drop(columns='Unnamed: 0', inplace=True)

# Print random 20 rows of the resulting data frame
print(df_union.sample(n=20, random_state=30, ignore_index=False))
