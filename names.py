# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

def add_prop(group):
    # integer 同士の除算は繰り上げ(floor)されてしまうため float にキャスト
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group

def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1
    


#birthdata = pd.read_table('enthought/pydata-book-master/ch02/names/yob1880.txt', sep=',', header=None, names=fieldname)

path = "enthought/pydata-book-master/ch02/names"
#filelist=os.listdir(path)
#filepaths = [path + '/' + fname for fname in filelist if re.match('^yob.*.txt$', fname)]

years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    targetpath = path + '/yob%d.txt' % year
    frame = pd.read_csv(targetpath, names=columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)

total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
#total_births.plot(title='Total births by sex and year')

names = names.groupby(['year', 'sex']).apply(add_prop)

top1000 = names.groupby(['year', 'sex']).apply(get_top1000)
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

#total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)
#subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
#subset.plot(subplots=True, figsize=(12, 10), grid=False, title="Number of births per year")

table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
#table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

df = boys[boys.year == 2010]
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

#diversity.plot(title='Number of popular names in top 50%')

get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)

subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
letter_prop = subtable / subtable.sum().astype(float)

fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)

letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
dny_ts.plot(style={'d':'-.', 'n':'-', 'y':':'})

all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()

table = filtered.pivot_table('births', index='year', columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
table.plot(style={'M': 'k-', 'F': 'k--'})
