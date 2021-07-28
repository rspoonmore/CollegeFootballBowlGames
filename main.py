import pandas as pd

rawResults = pd.read_excel('Results.xlsx')
rawConferences = pd.read_excel('conferences.xlsx')
results = rawResults.copy()

teamConferenceDetails = rawResults.merge(rawConferences, how='left', left_on=['School', 'Year'], right_on=['School', 'Year']).loc[:,['Conference', 'Division', 'Power Five']]
opponentConferenceDetails = rawResults.merge(rawConferences, how='left', left_on=['Opponent', 'Year'], right_on=['School', 'Year']).loc[:,['Conference', 'Division', 'Power Five']]
results['Team Conference'] = teamConferenceDetails['Conference']
results['Team Division'] = teamConferenceDetails['Division'] 
results['Team Power Five'] = teamConferenceDetails['Power Five'] 
results['Opponent Conference'] = opponentConferenceDetails['Conference']
results['Opponent Division'] = opponentConferenceDetails['Division'] 
results['Opponent Power Five'] = opponentConferenceDetails['Power Five'] 

print(results[results['Opponent Power Five'].isna()])
print(rawResults.loc[168,:])
print(teamConferenceDetails.loc[168,:])
print(opponentConferenceDetails.loc[168,:])

#print(results.info())
