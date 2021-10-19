import pandas as pd

df = pd.read_sql(
    '''
        select sd.t ,sd.y
        from signal_data sd
        where signal_id = 125 and
        sd.t between '2021-09-12 12:00:00' and '2021-09-12 13:00:00'
        order by sd.t
    ''',
    "postgresql://data_viewer:tokuapidemosystems@apidemo.tokusystems.com/new_mareland")

df_new = df.set_axis(['Last time', 'Amplitude'], axis=1, inplace=False)
df_new['Last time'] = pd.to_numeric(pd.to_datetime(df_new['Last time']))/100_000_0000

output = []

for i in range(0, len(df_new)):
    if i > 0 and i < (len(df_new)-1):
        da = (df_new['Amplitude'][i+1]-df_new['Amplitude'][i-1])
        dt = (df_new['Last time'][i+1]-df_new['Last time'][i-1])
        signal_rate = da/dt
        output.append(signal_rate)
    else:
        output.append('NaN')
output = pd.DataFrame(output)
output.append(df_new['Last time'])
output = output.set_axis(['Signal Rate'], axis=1, inplace=False)
print(output)
