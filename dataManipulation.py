from scipy import stats

# global variables
# ***************************************************************
decimal_places = 4

# general functions
# ***************************************************************

# general implementation of a recursive function.
# result must be passed in with every call to this function.
# It seems if result is not passed in, it can live as a closure
# with values from other function calls.


def implement_recursion(data, cb, result):
  if len(data) == 0:
    return result

  result.append(cb(data.pop(0)))
  return implement_recursion(data, cb, result)


def calculate_mean(data):
  return sum(data) / len(data)


# standard deviation of sample
def calculate_standard_deviation(data):
  return stats.tstd(data)


def calculate_z_score(data):
  raw_list = stats.zscore(data).tolist()
  return toNumPlaces(raw_list)


def toNumPlaces(data, places=decimal_places):
  return implement_recursion(data, lambda x: round(x, places), [])


# milage distribution
# ***************************************************************
def calc_milage_to_maintance(z_score):
  # we are assuming a few things here.
  # Primarily that 98% of cars on the road have travelled between 20000 and 80000 units (km or miles)
  full_result = 50000 + (z_score * 12931.0344)
  return round(full_result, decimal_places)


def calc_all_milages_to_maintance(z_scores):
  return implement_recursion(z_scores, lambda x: calc_milage_to_maintance(x), [])


# data manipulation functions
# ***************************************************************

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
