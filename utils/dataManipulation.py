from scipy import stats
from utils import ioOperators as io


# adds higher directory to python modules path
# allowing for quick and dirty import
import sys
sys.path.append("..")


# variables
# ***************************************************************
config_path = "config.json"
config = io.read_json_file(config_path)
decimal_places = config["decimal_places"]
mean_mileage = config["mean_mileage"]
mileage_std = config["mileage_std"]


# general functions
# ***************************************************************
# format a number to `digit` number of places.
# if `onlyFractional` is set to true, then return only the fractional part of the number
def to_number_of_places(data, digits=decimal_places, only_fractional=False, ):
  try:
    num = float(data)
  except:
    raise ValueError(
        "${0} is not a number. Please check your input.".format(data)
    )

  if only_fractional:
    num = num % 1

  return round(num, digits)


def round_list(data, places=decimal_places):
  return implement_recursion(data, lambda x: to_number_of_places(x, places), [])


# general implementation of a recursive function in which data
# from the array is popped off on each iteration. The result
# must be passed in with every call to this function. It seems
# that if result is not passed in, its value will not be
# implitly cleared and remain populated. I believe it will be
# treated as a global object.
def implement_recursion(data, cb, result, index=0):
  if len(data) == index:
    return result

  result.append(cb(data[0]))
  return implement_recursion(data, cb, result, index + 1)


# mathematical functions
# ***************************************************************
def calculate_mean(data):
  return sum(data) / len(data)


# standard deviation of sample
def calculate_standard_deviation(data):
  return stats.tstd(data)


def calculate_z_score(data):
  raw_list = stats.zscore(data).tolist()
  return round_list(raw_list)


# mileage distribution
# ***************************************************************
def calc_mileage_to_maintenance(z_score):
  # we are assuming a few things here.
  # Primarily that 98% of cars on the road have travelled between 20000 and 80000 units (km or miles)
  full_result = mean_mileage + (z_score * mileage_std)
  return round(full_result, decimal_places)


def calc_all_mileages_to_maintenance(z_scores):
  return implement_recursion(z_scores, lambda x: calc_mileage_to_maintenance(x), [])


# filter functions
# ***************************************************************
def key_exits(obj, key):
  if key in obj:
    return True
  return False


# returns the index of the first obj found in the list or -1 otherwise
def search_for(data, key, value, index=0):
  if len(data) == index:
    return -1

  current = data[index]
  if key_exits(current, key):
    if current[key] == value:
      return index

  return search_for(data, key, value, index + 1)


# returns an array of all the indices of the searched for object, key and value
def search_for_all(data, key, value, result, index=0):
  res_index = search_for(data, key, value, index)
  if res_index == -1:
    return result

  result.append(res_index)
  return search_for_all(data, key, value, result, res_index + 1)


# Receives in a dictionary and a list of keys or a single key.
# It will return the dictionary filtered by the specified params.
def filter_dict_by_param(data, params):
  return {key: data[key] for key in data.keys() if key in params}


# Receives in a list of dictionaries and a list of params and it will return
# a list of dictionaries filtered by those params. If the group_by and aggregate
# options are passed in, it will return a single dictionary with all of the specified
# values
def filter_list_by_param(data, params, group_by="", aggregate=False):
  if not aggregate:
    return [filter_dict_by_param(d_point, params) for d_point in data]

  if group_by not in params:
    print("The chosen aggregate value `groub_by` must be in the filtered list `params`")
    return False

  return {group_by: [filter_dict_by_param(d_point, params)[group_by] for d_point in data]}


# This assumes a dictionary with one single key.
# If a multikey dictionary is passed in, it will return the value of the first key
def get_dict_val(dictionary):
  key = [key for key in dictionary.keys()][0]
  return dictionary[key]


# this will append the `key` to every object
# in `data` with values in the same order as `values.`
# This will mutate the original `data` object
def append_prop_to_objs(data, key, values):
  for index, x in enumerate(data):
    x[key] = values[index]


# returns a list of items which matched the specified value.
# if `keepNonMatching` is set to True, the last item of this list
# will be set to a list containing all no-matching values
def aggregate_by_value(data, key, value, result, index=0, keepNonMatching=True):
  if len(data) == index:
    return result

  current = data[index]
  if current[key] == value:
    result.insert(0, current)

  if keepNonMatching and current[key] != value:
    # add obj to last item(which is a list of `other` values) of result
    result[-1].append(current)

  return aggregate_by_value(data, key, value, result, index + 1)


# aggregate mileage and energy values
def aggregate_values(data, clause, result):
  if len(data) == 0:
    return result

  current = data[0]
  aggregate_data = aggregate_by_value(data, clause, current[clause], [[]])
  # everything except last item
  values = aggregate_data[:-1]
  # last item which is a list of non-matching values
  data = aggregate_data[-1]

  trip_mileage = 0
  dissipation_value = 0
  for val in values:
    trip_mileage += val["trip_mileage"]
    dissipation_value += val["dissipation_value"]

  e_per_k = dissipation_value / trip_mileage
  current["trip_mileage"] = trip_mileage
  current["dissipation_value"] = dissipation_value
  current["e_per_k"] = round(e_per_k, 4)
  result.append(current)
  return aggregate_values(data, clause, result)
