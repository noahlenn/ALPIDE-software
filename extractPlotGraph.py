"""
Read data from influxdb database using dataframes
"""
import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt


# You can generate a Token from the "Tokens Tab" in the UI
bucket = "AlpideData"
org = "usn"
token = "ATwnh3qV6l95VXlCNJcnjQbpMiyyY3kpwn7JlluvhFLy4e_cPeB2HuqaEXJNxFXfldqcwKjcAVNh5zYGRFFFAA=="
url = "http://localhost:8086"

client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api = client.query_api()


data_frame = query_api.query_data_frame(f'from(bucket:"{bucket}")'
                                        '|> range(start: -2h)'
                                        '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
                                        '|> keep(columns: ["X", "Y", "Z"])')

pd_data_frame = pd.DataFrame(data_frame)  # Bruke Pandas for å behandle data

pd_data_frame.drop('result', inplace=True, axis=1); pd_data_frame.drop('table', inplace=True, axis=1)  # Fjern unødvendige kolonner
pd_data_frame.columns = ['X', 'Y', 'Z']  # Skriver X i stedet for x-coord, samme med Y og Z
print(f'\n{pd_data_frame}')  # Etter unødvendige kolonner fjernes og navn forbedres


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(pd_data_frame.X, pd_data_frame.Y, pd_data_frame.Z)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()



