
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions   #pip install influxdb-client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# You can generate an API token from the "API Tokens Tab" in the UI
token = "ATwnh3qV6l95VXlCNJcnjQbpMiyyY3kpwn7JlluvhFLy4e_cPeB2HuqaEXJNxFXfldqcwKjcAVNh5zYGRFFFAA=="
org = "usn"
bucket = "AlpideData"   #"AlpideData"
    
with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org,timeout=30_000) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS) 
    AlpideID=0x10
    seq=1
    
    xGlobal = int(input("X: "))
    yGlobal = int(input("Y: "))
    zGlobal = int(input("Z: "))
    #xGlobal=3000
    #yGlobal=2000
    #zGlobal=1000
    
    point = Point("Horten") \
            .tag(f"chipID={AlpideID}", f"seq={seq}") \
            .field("X",xGlobal ) \
            .field("Y",yGlobal ) \
            .field("Z",zGlobal ) \
            .time(datetime.utcnow(), WritePrecision.NS)
    
    data = []
    
    data.append(point)
    #insertString =f"Horten,chipID={AlpideID},seq={seq} X={x+(indx*1024)},Y={y+(indy*512)}" 
    #write_api.write(bucket, org, insertString)


    write_api.write(bucket, org, data)
          #write_api.write_points(data, database='AlpideData', time_precision='ms', batch_size=len(lst), protocol='line')            
          #insertString =f"Horten,chipID={AlpideID},seq={seq} cnt={len(lst)}"
          #write_api.write(bucket, org, insertString)
write_api.flush()
client.close()