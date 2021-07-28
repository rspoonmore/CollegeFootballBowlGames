import pandas as pd

rawResults = pd.read_excel('Results.xlsx')
rawConferences = pd.read_excel('conferences.xlsx')
results = rawResults.copy()
conferences = rawConferences.copy().groupby('Conference')['Year'].value_counts().to_frame().rename(columns={'Year': 'Teams'})

print('Results index is unique: %s' % results.index.is_unique)
print('Conference index is unique: %s' % rawConferences.index.is_unique)

results[['Team Conference', 'Team Division', 'Team Power Five']] = rawResults.merge(rawConferences, how='left', left_on=['School', 'Year'], right_on=['School', 'Year']).loc[:,['Conference', 'Division', 'Power Five']]
results[['Opponent Conference', 'Opponent Division', 'Opponent Power Five']] = rawResults.merge(rawConferences, how='left', left_on=['Opponent', 'Year'], right_on=['School', 'Year']).loc[:,['Conference', 'Division', 'Power Five']]

print('All games have team conference match: %s' % (results.count()['School'] == results.count()['Team Conference']))
print('All games have opponent conference match: %s' % (results.count()['School'] == results.count()['Opponent Conference']))

conferenceDescribe = results.groupby(['Year', 'Team Power Five', 'Team Conference']).describe().drop([('Opponent Points', 'count'), ('Team Pass', 'count'), ('Opponent Pass', 'count'), ('Team Rush', 'count'), ('Opponent Rush', 'count'), ('Opponent Yards', 'count'), ('Team Yards', 'count')], axis = 1)
DivisionDescribe = results.groupby(['Year', 'Team Power Five', 'Team Conference', 'Team Division']).describe().drop([('Opponent Points', 'count'), ('Team Pass', 'count'), ('Opponent Pass', 'count'), ('Team Rush', 'count'), ('Opponent Rush', 'count'), ('Opponent Yards', 'count'), ('Team Yards', 'count')], axis = 1)

results.insert(7, 'Win', results.apply(lambda x: x['Team Points'] > x['Opponent Points'], axis=1))

conferenceResults = results.groupby(['Team Conference', 'Year']).agg({'Bowl Game': 'count', 'Win': 'sum'}).rename(columns={'Bowl Game': 'Bowl Teams', 'Win':'Wins'})
conferenceResults.index = conferenceResults.index.rename(('Conference', 'Year'))

conferences[['Bowl Teams', 'Wins']] = conferences.merge(conferenceResults, how='inner', left_index=True, right_index=True).loc[:, ['Bowl Teams', 'Wins']]
conferences['Placeemnt %'] = conferences['Bowl Teams'] / conferences['Teams']
conferences['Win %'] = conferences['Wins'] / conferences['Bowl Teams']
print(conferences.head(1))

#print(conferenceDescribe.head(5))
