import os
import json
import subprocess
import psycopg2
import psycopg2.extras
import random as rn
import math


class Connector:
  def __init__(self, dbConfig):
    self._dbConfig = dbConfig

  def _establishConnection(self):
    try:
      return psycopg2.connect(
          dbname=self._dbConfig["dbName"],
          user=self._dbConfig["user"],
          password=self._dbConfig["password"],
          host=self._dbConfig["host"],
          port=self._dbConfig["port"]
      )
    except psycopg2.Error as e:
      if str(e.pgerror) != 'None':
        print(e.pgerror)
        print(e.diag.message_detail)
        raise ValueError()

  def closeConnection(self, connection):
    connection.close()

  def query(self, query):
    result = []
    try:
      # open connection per query
      conn = self._establishConnection()
      conn.autocommit = True
      # The cursor
      cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute(query)
      result = [dict(record) for record in cur]
    except psycopg2.Error as e:
      if str(e.pgerror) != 'None':
        print(e.pgerror)
        print(e.diag.message_detail)
      else:
        print("transaction success")

    finally:
      # close connection
      cur.close()
      conn.close()
    return result


# io functions
# ***************************************************************
def _open_file(file_path, mode, cb):
  with open(file_path, mode) as file_pointer:
    return cb(file_pointer)


def read_from_file(file_path, cb):
  return _open_file(file_path, "r", lambda _file: cb(_file))


# useful implementation to read from a json file
def read_json_file(file_path):
  return read_from_file(
      file_path,
      lambda _file: json.load(_file)
  )


# variables
# ***************************************************************
config_path = "config.json"
config = read_json_file(config_path)
decimal_places = config["decimal_places"]


# utility functions
# ***************************************************************
def sort_list_by(data, key, in_place=True, descending=False):
  try:
    if in_place:
      return data.sort(key=lambda x: x[key], reverse=descending)
    return sorted(data, key=lambda x: x[key], reverse=descending)
  except:
    print(
        "There was an error in sort_list_by. Data:{0}, key:{1}".format(data, key))


# format a number to `digit` number of places.
# if `onlyFractional` is set to true, then return only the fractional part of the number
def round_number(data, digits=decimal_places, only_fractional=False):
  try:
    num = float(data)
  except:
    raise ValueError(
        "${0} is not a number. Please check your input.".format(data)
    )

  if only_fractional:
    num = num % 1

  return round(num, digits)


# only takes in a number `value`
def num_of_digits(value):
  if value > 0:
    return int(math.log10(value))+1
  elif value == 0:
    return 1
  else:
    return int(math.log10(-value))+2  # +1 if you don't count the '-'


# only takes in a number `num`
def shift_left_by(num, places=None):
  if places is None:
    places = num_of_digits(num)
  return num / pow(10, places)


def split_acc_data_by_params(sensor_data):
  x = []
  y = []
  z = []
  timestamp = []

  for data_point in sensor_data:
    x.append(round_number(data_point["x"]))
    y.append(round_number(data_point["y"]))
    z.append(round_number(data_point["z"]))
    # t_interval is given as a whole number to save space by omitting
    # the 0s and decimals. Therefore, they need to be re-added here.
    fractional_timestamp = shift_left_by(float(data_point["t_interval"]))
    timestamp.append(round_number(fractional_timestamp))

  return {
      "x": x,
      "y": y,
      "z": z,
      "timestamp": timestamp
  }


def get_nested_property(obj, prop):
  try:
    nested = obj[prop]
  except:
    return obj
  else:
    return get_nested_property(nested, prop)


def filter_dict_by_param(data, params):
  return {key: data[key] for key in data.keys() if key in params}


# returns a filtered dictionary with keys taken from the params array.
# the value of each key is an array of aggregate items in the data list
# that share the same key. The shared _name property is the name
# of the property that you want to associate with every element of the array
def filter_list(data, params, shared_name, rename=""):
  if(len(rename) == 0):
    rename = shared_name

  shared_values = {}
  values = {}
  for element in data:
    shared_value = filter_dict_by_param(element, [shared_name])[shared_name]
    f_element = filter_dict_by_param(element, params)
    for key, value in f_element.items():
      try:
        shared_values[key].append(shared_value)
      except KeyError:
        shared_values[key] = [shared_value]

      try:
        values[key][rename] = shared_values[key]
        values[key]["values"].append(value)
      except KeyError:
        values[key] = {}
        values[key]["values"] = [value]

  return values


def get_filtered_data_obj(data, identifiers):
  result = {}
  for element in data:
    for identity in identifiers:
      if element["id"] != identity:
        continue

      try:
        result[identity].append(element["data"])
      except KeyError:
        result[identity] = element["data"]

  return result


def get_filtered_data_list(data, identifiers):
  f_list = []
  for element in data:
    if element["id"] not in identifiers:
      continue

    try:
      j_list = json.loads(element["data"])
    except ValueError:
      continue
    f_list.append(j_list)

  return f_list


# implementation
# ***************************************************************
def format_data(data, ids_to_format):
  aggregate_data = []
  prop_to_include = "deviceTimestamp"
  include = ids_to_format + [prop_to_include]
  for element in data:
    nested_data = get_nested_property(element, "data")
    f_data = get_filtered_data_obj(nested_data, include)
    # ignore empty entries
    if(len(f_data.items()) < 2):
      continue

    aggregate_data.append(f_data)

  sorted_list = sort_list_by(aggregate_data, prop_to_include, False)
  return filter_list(sorted_list, ids_to_format, prop_to_include, "timestamp")


# this function will format data passed in from the scanner_data_pid table.
# it will return a list of structured data in the following format:
# {
#   {
#     't_interval': [1577115015],
#     'dir': 'x',
#     'values': [0.05305481, -0.01808167, -0.01412964, 0.00686646, -0.02998352],
#     'timestamp': [0.112396, 0.39927, 0.479988, 0.680331, 0.880513]
#   },
#   {
#     't_interval': [1577115015],
#     'dir': 'y',
#     'values': [0.05303221, -0.01804367, -0.02332964, 0.044286646, -0.02997852],
#     'timestamp': [0.112396, 0.39927, 0.479988, 0.680331, 0.880513]
#   }, ...
# }
def format_accel_data(data, ids_to_format):
  final_res = []
  for element in data:
    nested_data = get_nested_property(element, "data")
    device_timestamp = get_filtered_data_list(nested_data, ["deviceTimestamp"])
    coordinates = get_filtered_data_list(nested_data, ids_to_format)
    for arr in coordinates:
      sorted_coor = sort_list_by(arr, "t_interval", False)
      # if there is an error sorting the data, ignore it as it is likely in an incorrect format
      if sorted_coor == None:
        continue

      coordinate_data = split_acc_data_by_params(sorted_coor)
      for key, value in coordinate_data.items():
        if key == "timestamp":
          continue

        result = {
            "t_interval": device_timestamp[0],
            "dir": key,
            "values": value,
            "timestamp": coordinate_data["timestamp"]
        }
        final_res.append(result)

  return final_res


# this function specifically obtains data from scanner_data_pid
# this is not a general function
def get_data(conn, vin, rtc_start, rtc_end):
  trip_query = "SELECT * FROM scanner_data_pid WHERE vin = '%s' and rtc_time >= %d and rtc_time <= %d limit 10" % (
      vin, rtc_start, rtc_end)

  return conn.query(trip_query)


def main():
  # dev = "local"
  dev = "staging"
  db_config = read_json_file("connector/config.json")[dev]
  conn = Connector(db_config)

  # vin = "JTMBK32V086045753"  # "2T1BU4EEXBC751673"  # "1G1JC5444R7252367"
  # rtc_start = 1578170804  # 1577113682  # 1573767218
  # rtc_end = 1578171833  # 1577115020  # 1573769218

  vin = "2T1BU4EEXBC751673"
  rtc_start = 1577113682
  rtc_end = 1577115020

  # This list contains the id values whose data property should formatted
  ids_to_format = ["accelerometer", "210D", "speed"]
  # ids_to_format = ["210C", "210F", "2142"]

  data = get_data(conn, vin, rtc_start, rtc_end)
  formatted_data = format_accel_data(data, ids_to_format)
  formatted_data_b = format_data(data, ["210C", "210F", "2142"])
  # formatted_data = format_data(data, ids_to_format)

  print(formatted_data)
  print("")
  print(formatted_data_b)


main()
