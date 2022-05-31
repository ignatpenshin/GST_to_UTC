import pandas as pd
import datetime
from tqdm import tqdm
import csv
import os

def GST_to_UTC(time_stamp):
    GST_start = datetime.datetime(1999, 8, 21, 23, 59, 42).timestamp()
    UTC_seconds = round(GST_start + time_stamp + 3*3600, 3)
    return UTC_seconds

def new_csv():
    csv_file = [i for i in os.listdir() if (i.startswith('tracktime') and len(i) > len('tracktime.csv'))][0]
    with open('tracktime.csv', 'w') as new:
        with open(csv_file) as file: 
            reader = csv.reader(file)
            new.write(next(reader)[0].replace('\t', ';') + '\n')
        df = pd.read_csv(csv_file, skiprows=1, sep = '	').assign(UTC_seconds = None)
        for index, row in tqdm(df.iterrows()):
            df.at[index,'UTC_seconds'] = GST_to_UTC(float(row['gpsTime']))

        x = tqdm(df.to_string(header=True,
                  index=False,
                  index_names=False).split('\n'))
        vals = [';'.join(ele.split()) for ele in x]
        for row in tqdm(vals):
            new.write(row + '\n')
    return df

new_csv()