from json import encoder
from os import scandir
import requests, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

file_path_json = './buildings.json'
file_path_jsonl = './buildings.jsonl'
file_path_csv = './buldings.csv'

scales =["220", "200-220", "180-200", "160-180", "140-160", "120-140", "100-120", "80-100", "60-80", "60"]
urls = []
df = pd.DataFrame(data=None, index=None, columns=['name','floor' ,'height', 'year', 'area'], dtype=None, copy=False)


for i in scales:
    urls.append('http://www.blue-style.com/database/scale-{}/'.format(i))
print(urls)
for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
   

    
    for i in soup.table.tbody.select('tr'):
        row = []
        row.append(i.select_one('th.name').text)
        
        for j in i.select('td'):
            row.append(j.text)
        
        df = df.append(pd.Series(row, index=df.columns), ignore_index=True)
        #print(pd.Series(row, index=df.columns))
        #print()

df['height'] = df['height'].replace('？m', np.nan)
df['height'] = df['height'].str[:-1].astype(float)

df['year'] = df['year'].replace('？年', np.nan)
df['year'] = df['year'].fillna("-1年")
df['year'] = df['year'].str[:-1].astype(int)
df['year'] = df['year'].replace(-1, np.nan)

#出力
df.to_csv(file_path_csv,  encoding='utf_8_sig')