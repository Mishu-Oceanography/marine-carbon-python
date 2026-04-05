import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. Load file

file = r"file path"
df = pd.read_excel(file)


# 2. Clean column names

df.columns = df.columns.str.strip()

# --------------------------------------------------
# 3. Convert Date column to datetime

df['Date'] = pd.to_datetime(df['Date [MM/DD/YYYY]'])


# 4. Clean pCO2 columns

df['pCO2_SW_sat [uatm]'] = (
    df['pCO2_SW_sat [uatm]']
    .astype(str)
    .str.strip()
    .replace(['-999', '-9999', '-99', '--', ''], np.nan)
)

df['pCO2_Air_sat [uatm]'] = (
    df['pCO2_Air_sat [uatm]']
    .astype(str)
    .str.strip()
    .replace(['-999', '-9999', '-99', '--', ''], np.nan)
)

# Convert to numeric
df['pCO2_SW_sat [uatm]'] = pd.to_numeric(df['pCO2_SW_sat [uatm]'], errors='coerce')
df['pCO2_Air_sat [uatm]'] = pd.to_numeric(df['pCO2_Air_sat [uatm]'], errors='coerce')

# 5. Set Date as index

df = df.set_index('Date')
df = df.sort_index()


# 6. Convert to Daily Mean (IMPORTANT)

daily = df.resample('D').mean()


# 7. Plot Time Series

plt.figure(figsize=(14,6))

plt.plot(daily.index, daily['pCO2_SW_sat [uatm]'], label='Surface pCO2')
plt.plot(daily.index, daily['pCO2_Air_sat [uatm]'], label='Air pCO2')

plt.xlabel('Time')
plt.ylabel('pCO2 (µatm)')
plt.title('Air–Sea pCO2 Time Series')
plt.legend()

plt.tight_layout()
plt.show()

