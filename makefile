# download bike crash data to ./data/nyc_bike_crashes.csv if it doesn't exist
data/nyc_bike_crashes.csv : data/nyc_bike_crashes.csv
ifdef SODAPY_APPTOKEN
	./retrieve_nyc_crashes_soda.py --token $(SODAPY_APPTOKEN) data/nyc_bike_crashes.csv
else
	./retrieve_nyc_crashes_soda.py data/nyc_bike_crashes.csv
endif
