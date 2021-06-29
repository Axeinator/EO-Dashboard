from fastapi import FastAPI
from load_file import load_ports
from helpers import get_forecast, get_horizontal_wind, get_vert_wind, get_risk_level
import pandas as pd
app = FastAPI()

ports_df = load_ports()

no2_df = pd.DataFrame()

for row in ports_df.iterrows():
	row = row[1]
	print(row.Name)
	fc = get_forecast(row.lat, row.lon)
	speed_1000, speed_925, speed_850 = get_horizontal_wind(fc)
	v_speed_1000, v_speed_925, v_speed_850 = get_vert_wind(fc)
	risk = get_risk_level(speed_1000, v_speed_1000)
	res = dict(LOCODE=row.LOCODE, risk=risk)
	no2_df.append(res, ignore_index=True)
no2_df.to_csv('no2_res.csv')
