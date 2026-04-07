import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------
file = r"E:\DATASETS\RAMA DATA\RAMA_PCO2CSV\rama13-21.xls"
df = pd.read_excel(file)

# Clean column names
df.columns = df.columns.str.strip()

# Convert Date column
df['Date'] = pd.to_datetime(df['Date [MM/DD/YYYY]'], errors='coerce')

# Keep only required columns
df = df[['Date',
         'pCO2_Air_sat [uatm]',
         'pCO2_SW_sat [uatm]']]

# Rename for simplicity
df.rename(columns={
    'pCO2_Air_sat [uatm]': 'Air_pCO2',
    'pCO2_SW_sat [uatm]': 'Sea_pCO2'
}, inplace=True)

# Drop missing dates
df = df.dropna(subset=['Date'])

# --------------------------------------------------
# 2. REMOVE PHYSICALLY IMPOSSIBLE + UNREALISTIC VALUES
# --------------------------------------------------
for col in ['Air_pCO2', 'Sea_pCO2']:

    # Convert to numeric
    df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove negative and zero values
    df.loc[df[col] <= 0, col] = np.nan

    # Apply realistic open-ocean range filter
    df.loc[df[col] < 250, col] = np.nan
    df.loc[df[col] > 600, col] = np.nan

# --------------------------------------------------
# 3. REMOVE STATISTICAL OUTLIERS (IQR METHOD)
# --------------------------------------------------
def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    data.loc[(data[column] < lower_bound) |
             (data[column] > upper_bound), column] = np.nan

    return data

df = remove_outliers_iqr(df, 'Air_pCO2')
df = remove_outliers_iqr(df, 'Sea_pCO2')

# --------------------------------------------------
# 4. SORT & SET DATE INDEX
# --------------------------------------------------
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# --------------------------------------------------
# 5. RESAMPLE (Daily or Monthly)
# --------------------------------------------------
df_resampled = df.resample('D').mean()
# df_resampled = df.resample('M').mean()

# --------------------------------------------------
# 6. PLOT CLEAN TIME SERIES
# --------------------------------------------------
plt.figure(figsize=(12, 6))

plt.plot(df_resampled.index,
         df_resampled['Sea_pCO2'],
         label='Surface pCO₂',
         linewidth=1.5)

plt.plot(df_resampled.index,
         df_resampled['Air_pCO2'],
         label='Air pCO₂',
         linewidth=1.5)

plt.title('Time Series of Air–Sea pCO₂', fontsize=14)
plt.xlabel('Time')
plt.ylabel('pCO₂ (µatm)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


