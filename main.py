import pandas as pd
from BowlExcelCreator import createBowlExcel
from DashboardBuilder import createDashboard

excelFileName = "Generated Files/College Football Bowl Game Analysis.xlsx"
dashFileName = "Generated Files/College Football Bowl Game Analysis Dashboard.pdf"

[results, conferences, divisions] = createBowlExcel(excelFileName)
createDashboard(results, conferences, divisions, plotStyle='seaborn-colorblind', dashboardFileName=dashFileName)

