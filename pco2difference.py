import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Load Excel file
# --------------------------------------------------
file = r"E:\DATASETS\RAMA DATA\RAMA_PCO2CSV\ramapCO2_dec14-jun15.xls"
df = pd.read_excel(file)

# --------------------------------------------------
# 2. Clean column names
# --------------------------------------------------
df.columns = df.columns.str.strip()

# --------------------------------------------------
# 3. Convert Date column to datetime
# --------------------------------------------------
df['Date'] = pd.to_datetime(df['Date [MM/DD/YYYY]'])

# --------------------------------------------------
# 4. Clean pCO2 columns
# --------------------------------------------------
for col in ['pCO2_SW_sat [uatm]', 'pCO2_Air_sat [uatm]']:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .replace(['-999', '-9999', '-99', '--', ''], np.nan)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --------------------------------------------------
# 5. Set Date as index
# --------------------------------------------------
df = df.set_index('Date')
df = df.sort_index()

# --------------------------------------------------
# 6. Convert to daily mean
# --------------------------------------------------
daily = df.resample('D').mean()

# --------------------------------------------------
# 7. Calculate ΔpCO2
# --------------------------------------------------
daily['delta_pCO2'] = (
    daily['pCO2_SW_sat [uatm]'] -
    daily['pCO2_Air_sat [uatm]']
)

# --------------------------------------------------
# 8. Plot ΔpCO2 time series
# --------------------------------------------------
plt.figure(figsize=(14,6))

plt.plot(daily.index, daily['delta_pCO2'], label='ΔpCO2 (Sea - Air)')

plt.axhline(0, linestyle='--', color='black')  # zero reference line

plt.xlabel('Time')
plt.ylabel('ΔpCO2 (µatm)')
plt.title('Air–Sea pCO2 Difference')
plt.legend()

plt.tight_layout()
plt.show()