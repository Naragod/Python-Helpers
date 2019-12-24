
# *************************************************************************


# def get_connection(db_name):
#   dbConfig = config.configuration[db_name]
#   return connector.Connector(dbConfig)


# def get_car_data(db_name, vin, rtc_start, rtc_end):
#   connection = get_connection(db_name)
#   output_trip_mileage = 0

#   trip_query = "SELECT * FROM scanner_data_trip WHERE vin = '%s' and rtc_time_start = %d and rtc_time_end = %d" % (
#       vin, rtc_start, rtc_end)

#   result = connection.query(trip_query)
#   if len(result) == 0:
#     print('no records found in that time range %d' % (rtc_end - rtc_end))
#   elif len(result) == 1:
#     output_trip_mileage = result[0]['mileage']
#     # logger.info('mileage found successfully')
#     print('mileage found successfully')
#   else:
#     # logger.info('more than one record found when retrieving mileage')
#     # logger.info('setting trip mileage to 0 (default)')
#     print('more than one record found when retrieving mileage')
#     print('setting trip mileage to 0 (default)')

#   return output_trip_mileage


# db_name = "staging"
# rtc_time_start = 1503521399
# rtc_time_end = 1503521500
# vin = "2T1BR32E87C850175"


# query = "Select * from scanner_data_trip limit 1"
# ci = get_connection("staging")
# result = ci.query(query)

# result = get_car_data(db_name, vin, rtc_time_start, rtc_time_end)