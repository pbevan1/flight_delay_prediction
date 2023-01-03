import os
import pandas as pd

root = "data/"

filenames = []

for path, subdirs, files in os.walk(root):
    for name in files:
        filenames.append(os.path.join(path, name))

dfs = []

[ dfs.append(pd.read_csv(f)) for f in filenames ]

df_subs = []
for i, df in enumerate(dfs):
    print(filenames[i])
    if 'departure.terminal' not in df.columns:
        df['departure.terminal'] = None
    if 'departure.gate' not in df.columns:
        df['departure.gate'] = None
    # Add in column for airport by extracting from filename

    df_sub = df[['airline.name', 'departure.terminal', 'departure.gate',
    'departure.scheduledTime', 'status', 'departure.iataCode', 'arrival.delay', 'arrival.iataCode']]
    df_subs.append(df_sub)

combined_csv = pd.concat(df_subs)
combined_csv.to_csv('data/2022/flights_combined.csv', index=False)
