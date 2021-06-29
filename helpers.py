import getgfs
from metpy.calc import wind_speed, wind_direction
from metpy.units import units
from datetime import datetime

def get_forecast(lat, lon):
	
	now = datetime.utcnow().strftime('%Y%m%d 06:00')
	f = getgfs.Forecast("0p25")

	return f.get(["ugrdprs", "vgrdprs", "dzdtprs"], now, lat, lon)

def get_horizontal_wind(forecast):
	res = forecast
	u_speed_1000 = res.variables['ugrdprs'].data[0][0]
	v_speed_1000 = res.variables['vgrdprs'].data[0][0]

	u_speed_925 = res.variables['ugrdprs'].data[0][3]
	v_speed_925 = res.variables['vgrdprs'].data[0][3]

	u_speed_850 = res.variables['ugrdprs'].data[0][5]
	v_speed_850 = res.variables['vgrdprs'].data[0][5]

	u_speed_1000 = units.Quantity(u_speed_1000, 'm/s')
	v_speed_1000 = units.Quantity(v_speed_1000, 'm/s')

	u_speed_925 = units.Quantity(u_speed_925, 'm/s')
	v_speed_925 = units.Quantity(v_speed_925, 'm/s')

	u_speed_850 = units.Quantity(u_speed_850, 'm/s')
	v_speed_850 = units.Quantity(v_speed_850, 'm/s')



	wind_speed_1000 = wind_speed(u_speed_1000, v_speed_1000).m_as('knots').flatten()[0]
	wind_speed_925 = wind_speed(u_speed_925, v_speed_925).m_as('knots').flatten()[0]
	wind_speed_850 = wind_speed(u_speed_850, v_speed_850).m_as('knots').flatten()[0]
	return (wind_speed_1000, wind_speed_925, wind_speed_850)

def get_vert_wind(forecast):
	res = forecast
	vert_velocity_1000 = res.variables['dzdtprs'].data[0][0]
	vert_velocity_925 = res.variables['dzdtprs'].data[0][3]
	vert_velocity_850 = res.variables['dzdtprs'].data[0][5].flatten()
	return [vert_velocity_1000, vert_velocity_925, vert_velocity_850]

# Only take risk levels from the lowest level of the atmosphere
def get_risk_level(vert_velocity_1000, wind_speed_1000):
	risk_level = ""

	if vert_velocity_1000 < -0.05 and wind_speed_1000 < 7.5: # worst conditions, not moving upwards, or away
			risk_level = "red"
	elif vert_velocity_1000 > -0.05 and wind_speed_1000 < 7.5: # better, no2 is moving up, but not away
			risk_level = "orange"
	elif vert_velocity_1000 < -0.05 and wind_speed_1000 > 7.5: # better than before, moving away, but not up
			risk_level = "yellow"
	elif vert_velocity_1000 > -0.05 and wind_speed_1000 > 7.5: # no2 is moving up and away
			risk_level = "green"

	return risk_level, vert_velocity_1000, wind_speed_1000

