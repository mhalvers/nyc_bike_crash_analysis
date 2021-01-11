# download bike crash data to ./data/nyc_bike_crashes.csv if it doesn't exist
data/nyc_bike_crashes.csv : data/nyc_bike_crashes.csv
	./retrieve_nyc_crashes_soda.py $(SODAPY_APPTOKEN) data/nyc_bike_crashes.csv

