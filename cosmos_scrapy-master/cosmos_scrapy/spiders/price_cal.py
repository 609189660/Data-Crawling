import pandas as pd

df=pd.read_csv('price_cal.csv')
print(df.groupby('Engine_Code')['price'].median())
print(df['Engine_Code'].drop_duplicates())

ans=[]
for i in range(0,321):
    price=df.groupby('Engine_Code')['price'].median()[i]




