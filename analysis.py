import pandas as pd


# write your code here
pd.set_option('display.max_columns', 8)

df_general = pd.read_csv('test/general.csv')
print(df_general.head(20))

df_prenatal = pd.read_csv('test/prenatal.csv')
print(df_prenatal.head(20))

df_sport = pd.read_csv('test/sports.csv')
print(df_sport.head(20))
