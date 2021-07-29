import pandas as pd

def createBowlExcel(excelFileName):
    rawResults = pd.read_excel("Data Files/Results.xlsx")
    rawConferences = pd.read_excel("Data Files/conferences.xlsx", sheet_name="Sheet1")
    results = rawResults.copy()
    conferences = rawConferences.copy().groupby('Year')['Conference'].value_counts().to_frame().rename(columns={'Conference': 'Teams'})
    divisions = rawConferences.copy().groupby(['Year', 'Conference'])['Division'].value_counts().to_frame().rename(columns={'Division': 'Teams'})

    print('Results index is unique: %s' % results.index.is_unique)
    print('Conference index is unique: %s' % rawConferences.index.is_unique)

    results[['Team Conference', 'Team Division', 'Team Power Five']] = rawResults.merge(rawConferences, how='left', left_on=['School', 'Year'], right_on=['School', 'Year']).loc[:,['Conference', 'Division', 'Power Five']]
    results[['Opponent Conference', 'Opponent Division', 'Opponent Power Five']] = rawResults.merge(rawConferences, how='left', left_on=['Opponent', 'Year'], right_on=['School', 'Year']).loc[:,['Conference', 'Division', 'Power Five']]

    print('All games have team conference match: %s' % (results.count()['School'] == results.count()['Team Conference']))
    print('All games have opponent conference match: %s' % (results.count()['School'] == results.count()['Opponent Conference']))

    # Create DF of conferences and devisions with describe() 
    resultsDescribe = results.describe().drop('Year', axis=1)
    conferenceDescribe = results.groupby(['Year', 'Team Power Five', 'Team Conference']).describe().drop([('Team Points', 'count'), ('Opponent Points', 'count'), ('Team Pass', 'count'), ('Opponent Pass', 'count'), ('Team Rush', 'count'), ('Opponent Rush', 'count'), ('Opponent Yards', 'count'), ('Team Yards', 'count')], axis = 1)
    divisionDescribe = results.groupby(['Year', 'Team Power Five', 'Team Conference', 'Team Division']).describe().drop([('Team Points', 'count'), ('Opponent Points', 'count'), ('Team Pass', 'count'), ('Opponent Pass', 'count'), ('Team Rush', 'count'), ('Opponent Rush', 'count'), ('Opponent Yards', 'count'), ('Team Yards', 'count')], axis = 1)
    conferenceDescribe.index = conferenceDescribe.index.rename(['Year', 'Power Five', 'Conference'])
    divisionDescribe.index = divisionDescribe.index.rename(['Year', 'Power Five', 'Conference', 'Division'])
    conferenceDescribe.columns = [' '.join(col) for col in conferenceDescribe.columns.values]
    divisionDescribe.columns = [' '.join(col) for col in divisionDescribe.columns.values]
    conferenceDescribe.reset_index('Power Five', inplace=True)
    divisionDescribe.reset_index('Power Five', inplace=True)

    # Add win boolean
    results.insert(7, 'Win', results.apply(lambda x: x['Team Points'] > x['Opponent Points'], axis=1))
    results.insert(7, 'Point Diff', results['Team Points'] - results['Opponent Points'])

    # Create DF of conference and dvision placement and Win percentage and add to describes
    conferencePlacement = results.loc[:, ['Year', 'Team Conference', 'School']].drop_duplicates().groupby(['Year', 'Team Conference']).count().rename(columns={'School': 'Bowl Teams'})
    conferencePlacement.index = conferencePlacement.index.rename(('Year', 'Conference'))
    conferenceResults = results.groupby(['Year', 'Team Conference']).agg({'Bowl Game': 'count', 'Win': 'sum'}).rename(columns={'Bowl Game': 'Bowl Games', 'Win':'Wins'})
    conferenceResults.index = conferenceResults.index.rename(('Year', 'Conference'))
    conferences['Bowl Teams'] = conferences.merge(conferencePlacement, how='inner', left_index=True, right_index=True).loc[:, 'Bowl Teams']
    conferences[['Bowl Games', 'Wins']] = conferences.merge(conferenceResults, how='inner', left_index=True, right_index=True).loc[:, ['Bowl Games', 'Wins']]
    conferences['Placement %'] = conferences['Bowl Teams'] / conferences['Teams']
    conferences['Win %'] = conferences['Wins'] / conferences['Bowl Games']
    conferences = conferences.merge(conferenceDescribe, how='left', left_index=True, right_index=True)

    divisionPlacement = results.loc[:, ['Year', 'Team Conference', 'Team Division', 'School']].drop_duplicates().groupby(['Year', 'Team Conference', 'Team Division']).count().rename(columns={'School': 'Bowl Teams'})
    divisionPlacement.index = divisionPlacement.index.rename(['Year', 'Conference', 'Division'])
    divisionResults = results.groupby(['Year', 'Team Conference', 'Team Division']).agg({'Bowl Game': 'count', 'Win': 'sum'}).rename(columns={'Bowl Game': 'Bowl Games', 'Win':'Wins'})
    divisionResults.index = divisionResults.index.rename(['Year', 'Conference', 'Division'])
    divisions['Bowl Teams'] = divisions.merge(divisionPlacement, how='inner', left_index=True, right_index=True).loc[:, 'Bowl Teams']
    divisions[['Bowl Games', 'Wins']] = divisions.merge(divisionResults, how='inner', left_index=True, right_index=True).loc[:, ['Bowl Teams', 'Wins']]
    divisions['Placement %'] = divisions['Bowl Teams'] / divisions['Teams']
    divisions['Win %'] = divisions['Wins'] / divisions['Bowl Games']
    divisions = divisions.merge(divisionDescribe, how='left', left_index=True, right_index=True)

    # Save DFs to excel
    writer = pd.ExcelWriter(excelFileName, engine='xlsxwriter')
    results.to_excel(writer, sheet_name="Game Results", engine="xlsxwriter", index=False)
    conferences.to_excel(writer, sheet_name='Conference Results', engine='xlsxwriter')
    divisions.to_excel(writer, sheet_name='Division Results', engine='xlsxwriter')
    writer.save()

    return [results, conferences, divisions]