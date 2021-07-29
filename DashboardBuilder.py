import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sb
import numpy as np

def findQuad(row):
    if row['Difference in Rushing Yards'] >= 0 and row['Difference in Passing Yards'] >= 0:
        return 'Both Positive'
    elif row['Difference in Rushing Yards'] >= 0 and row['Difference in Passing Yards'] < 0:
        return 'Only Rush Positive'
    elif row['Difference in Rushing Yards'] < 0 and row['Difference in Passing Yards'] >= 0:
        return 'Only Pass Positive'
    elif row['Difference in Rushing Yards'] < 0 and row['Difference in Passing Yards'] < 0:
        return 'Both Negative'


# results = pd.read_excel('College Football Bowl Game Analysis.xlsx', sheet_name='Game Results')
# conferences = pd.read_excel('College Football Bowl Game Analysis.xlsx', sheet_name='Conference Results', index_col=[0, 1]).reset_index(['Year', 'Conference'])
# divisions = pd.read_excel('College Football Bowl Game Analysis.xlsx', sheet_name='Division Results', index_col=[0, 1, 2]).reset_index(['Year', 'Conference', 'Division'])

def createDashboard(results, conferences, divisions, plotStyle, dashboardFileName):
    plt.style.use(plotStyle)

    conferences.reset_index(['Year', 'Conference'], inplace=True)
    divisions.reset_index(['Year', 'Conference', 'Division'], inplace=True)
    results['Result'] = results['Win'].apply(lambda x: 'Win' if x else 'Lose')
    results['Difference in Rushing Yards'] = results['Team Rush'] - results['Opponent Rush']
    results['Difference in Passing Yards'] = results['Team Pass'] - results['Opponent Pass']
    results['Yardage Difference Quadrant'] = results.apply(lambda row: findQuad(row), axis=1)
    QuadResults = results.groupby('Yardage Difference Quadrant').agg({'Bowl Game': 'count', 'Win': 'sum'})
    QuadResults['Win %'] = QuadResults['Win'] / QuadResults['Bowl Game']

    print(QuadResults)

    PFiveResults = results[results['Team Power Five'] == 'Power Five']
    # PFiveWinners = PFiveResults[PFiveResults['Win']]
    # PFiveLosers = PFiveResults[~PFiveResults['Win']]

    fig = plt.figure(figsize=(30, 30))
    gs = GridSpec(4, 6, figure=fig)
    ax1 = fig.add_subplot(gs[0, :3])
    ax2 = fig.add_subplot(gs[0, 3:])
    ax3 = fig.add_subplot(gs[1, :3])
    ax4 = fig.add_subplot(gs[1, 3:])
    ax5 = fig.add_subplot(gs[3, 2:4])
    ax6 = fig.add_subplot(gs[3, 4:])
    ax7 = fig.add_subplot(gs[2, :2])
    ax8 = fig.add_subplot(gs[3, :2])
    ax9 = fig.add_subplot(gs[2, 2:])


    # Difference in Pass vs Rush Yards Scatter
    lowerLimit = min(min(PFiveResults['Difference in Rushing Yards']) - 10, min(PFiveResults['Difference in Passing Yards']) - 10, -300)
    upperLimit = max(max(PFiveResults['Difference in Rushing Yards']) + 10, max(PFiveResults['Difference in Passing Yards']) + 10, 300)

    sb.scatterplot(x=PFiveResults['Difference in Rushing Yards'], y=PFiveResults['Difference in Passing Yards'], hue=PFiveResults['Team Conference'], ax=ax1, style=PFiveResults['Result'], s=150)
    ax1_copy = ax1.twinx()
    ax1.set_xlim(lowerLimit, upperLimit)
    ax1.set_ylim(lowerLimit, upperLimit)
    ax1_copy.set_xlim(lowerLimit, upperLimit)
    ax1_copy.set_ylim(lowerLimit, upperLimit)
    ax1.set_title('Difference in Rushing Yards vs Difference in Passing Yards (Power Five)')
    lineBase = np.linspace(lowerLimit, upperLimit, 10)

    ax1_copy.plot(lineBase, [0] * len(lineBase), 'k--')
    ax1_copy.plot([0] * len(lineBase), lineBase, 'k--')

    # Points Scored Box
    sb.boxplot(data=PFiveResults, x='Year', y='Team Points', hue='Team Conference', ax=ax2)
    handles, labels = ax2.get_legend_handles_labels()
    sb.stripplot(data=PFiveResults, x='Year', y='Team Points', dodge=True, hue='Team Conference', color='black', linewidth=0, ax=ax2)
    ax2.set_title('Points Scored by Conference Each Year (Power Five)')
    ax2.legend(handles, labels)
    # ax2.legend(loc='upper left')

    # Rush Yards Box
    sb.boxplot(data=PFiveResults[PFiveResults['Year'] > 2018], x='Year', y='Team Rush', hue='Team Conference', ax=ax3)
    handles, labels = ax3.get_legend_handles_labels()
    sb.stripplot(data=PFiveResults[PFiveResults['Year'] > 2018], x='Year', y='Team Rush', dodge=True, hue='Team Conference', color='black', linewidth=0, ax=ax3)
    ax3.set_title('Rushing Yards by Conference Each Year (Power Five)')
    ax3.legend(handles, labels)
    # ax2.legend(loc='upper left')

    # Pass Yards Box
    sb.boxplot(data=PFiveResults[PFiveResults['Year'] > 2018], x='Year', y='Team Pass', hue='Team Conference', ax=ax4)
    handles, labels = ax4.get_legend_handles_labels()
    sb.stripplot(data=PFiveResults[PFiveResults['Year'] > 2018], x='Year', y='Team Pass', dodge=True, hue='Team Conference', color='black', linewidth=0, ax=ax4)
    ax4.set_title('Passing Yards by Conference Each Year (Power Five)')
    ax4.legend(handles, labels)
    # ax2.legend(loc='upper left')

    # Win Pie Chart
    totalConferenceWins = conferences.groupby('Conference').agg({'Wins': 'sum'}).reset_index('Conference')
    ax5.pie(totalConferenceWins['Wins'], labels=totalConferenceWins['Conference'], autopct='%1.1f%%')
    ax5.set_title('Percent of Wins by Conference')

    # Win Pie Chart
    totalPFiveConferenceWins = conferences[conferences['Power Five'] == 'Power Five'].groupby('Conference').agg({'Wins': 'sum'}).reset_index('Conference')
    ax6.pie(totalPFiveConferenceWins['Wins'], labels=totalPFiveConferenceWins['Conference'], autopct='%1.1f%%')
    ax6.set_title('Percent of Wins by Conference (Power Five)')

    # Win % Heatmap
    conferenceWinPercByYear = pd.pivot_table(conferences, values=['Win %'], index=['Conference'], columns=['Year']).apply(lambda x: 100 * x).round(2)
    conferenceWinPercByYear.columns = conferenceWinPercByYear.columns.get_level_values('Year')

    sb.heatmap(data=conferenceWinPercByYear, annot=True, center=50, fmt='g', ax=ax7, cmap='RdYlGn', vmin=0, vmax=100)
    ax7.set_title('Win Percentage by Conference Each Year')


    # Placement % Heatmap
    conferencePlacePercByYear = pd.pivot_table(conferences, values=['Placement %'], index=['Conference'], columns=['Year']).apply(lambda x: 100 * x).round(2)
    conferencePlacePercByYear.columns = conferencePlacePercByYear.columns.get_level_values('Year')

    sb.heatmap(data=conferencePlacePercByYear, annot=True, fmt='g', ax=ax8, cmap='RdYlGn', vmin=0, vmax=100)
    ax8.set_title('Placement Percentage by Conference Each Year')


    # Win Total By Conference
    # [conferences['Power Five'] == 'Power Five']
    sb.barplot(data=conferences, x='Year', y='Wins', hue='Conference', ax=ax9, palette=sb.color_palette())
    ax9.set_title('Wins by Conference Each Year')
    ax9.legend(fontsize='small')


    plt.suptitle('College Footbal Bowl Game Analysis Dashboard', fontsize=50)
    # Add some space between subplots
    plt.subplots_adjust(wspace=.3)
    plt.savefig(dashboardFileName)
