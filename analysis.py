import pandas as pd

# Read CSV files with datasets
pd.set_option('display.max_columns', 8)
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
values = {'bmi': 0, 'diagnosis': 0, 'blood_test': 0, 'ecg': 0, 'ultrasound': 0, 'mri': 0, 'xray': 0, 'children': 0, 'months': 0}
df_union.fillna(value=values,  inplace=True)

# Print random 20 rows of the resulting data frame
print(df_union.shape)
print(df_union.sample(n=20, random_state=30, ignore_index=False))
