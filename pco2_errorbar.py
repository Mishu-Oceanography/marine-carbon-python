import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. LOAD DATA
file = r"E:\DATASETS\RAMA DATA\RAMA_PCO2CSV\rama13-21.xls"
df = pd.read_excel(file)

# Clean column names
df.columns = df.columns.str.strip()

# 2. CONVERT DATE COLUMN
df['Date'] = pd.to_datetime(df['Date [MM/DD/YYYY]'], errors='coerce')

# Keep required columns
df = df[['Date',
         'pCO2_Air_sat [uatm]',
         'pCO2_SW_sat [uatm]']]

# Rename columns
df.rename(columns={
    'pCO2_Air_sat [uatm]': 'Air_pCO2',
    'pCO2_SW_sat [uatm]': 'Sea_pCO2'
}, inplace=True)

# Drop missing dates
df = df.dropna(subset=['Date'])

# 3. CLEAN pCO2 VALUES
for col in ['Air_pCO2', 'Sea_pCO2']:

    df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove physically unrealistic values
    df.loc[df[col] <= 0, col] = np.nan
    df.loc[df[col] < 250, col] = np.nan
    df.loc[df[col] > 600, col] = np.nan

# 4. SORT & SET DATE AS INDEX
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# 🔎 Check if index is datetime (optional check)
print(type(df.index))   # should show DatetimeIndex

# 5.MONTHLY CLIMATOLOGY (Average all years together)

# Group by month number (1–12)
clim_mean = df.groupby(df.index.month).mean()
clim_std  = df.groupby(df.index.month).std()

plt.figure(figsize=(10,6))

plt.errorbar(clim_mean.index,
             clim_mean['Sea_pCO2'],
             yerr=clim_std['Sea_pCO2'],
             fmt='s',
             color='blue',      # marker color
             ecolor='red',      # error bar color
             capsize=5,
             linewidth=1.5)

plt.xticks(range(1,13),
           ['J','F','M','A','M','J','J','A','S','O','N','D'])

plt.ylabel('pCO₂ (µatm)')
plt.xlabel('Months')
plt.title('Mean Surface pCO₂ (RAMA)')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()