import pandas as pd
import matplotlib.pyplot as plt
# import GridSpec as gs
import seaborn as sb
from BowlExcelCreator import createBowlExcel

excelFileName = 'College Football Bowl Game Analysis.xlsx'

[results, conferences, divisions] = createBowlExcel(excelFileName)

fig = plt.figure()
sb.boxplot(data=results[results['Team Power Five'] == 'Power Five'], x='Year', y='Team Points', hue='Team Conference')
plt.show()
#print(resultsDescribe)