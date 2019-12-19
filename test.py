from connector import connector
from connector import config



# *************************************************************************
def get_connection(db_name):
  dbConfig = config.configuration[db_name]

  return connector.Connector(dbConfig)

# def get_car_data(db_name, vin, rtc_start, rtc_end):
#   connection = get_connection(db_name)
#   output_trip_mileage = 0

#   trip_query = "SELECT * FROM scanner_data_trip WHERE vin = '%s' and rtc_time_start = %d and rtc_time_end = %d" % (
#       vin, rtc_start, rtc_end)

#   result = connection.(query=trip_query, env_db=db_name)
#   if len(result) == 1:
#     output_trip_mileage = result[0]['mileage']
#     logger.info('mileage found successfully')
#   else:
#     logger.info('more than one record found when retrieving mileage')
#     logger.info('setting trip mileage to 0 (default)')

#   return output_trip_mileage


query = "Select id, vin from car limit 10"
ci = get_connection("staging")
result = ci.query(query)
print(result)