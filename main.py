import pandas as pd
from BowlExcelCreator import createBowlExcel
from DashboardBuilder import createDashboard

excelFileName = 'College Football Bowl Game Analysis.xlsx'

[results, conferences, divisions] = createBowlExcel(excelFileName)
createDashboard(results, conferences, divisions, plotStyle='seaborn-colorblind')

