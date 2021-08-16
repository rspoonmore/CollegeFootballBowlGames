import pandas as pd
from BowlExcelCreator import createBowlExcel
from DashboardBuilder import createDashboard
import seaborn as sb
import matplotlib.pyplot as plt

excelFileName = "Generated Files/College Football Bowl Game Analysis.xlsx"
dashFileNames = ["Generated Files/High Level College Football Bowl Game Analysis Dashboard.pdf", "Generated Files/Division Level College Football Bowl Game Analysis Dashboard.pdf"]

[results, conferences, divisions] = createBowlExcel(excelFileName)
createDashboard(results, conferences, divisions, plotStyle='seaborn-colorblind', dashboardFileNames=dashFileNames)

