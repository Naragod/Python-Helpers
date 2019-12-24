from scipy import stats

# general functions
# ***************************************************************
def calculate_mean(data):
  return sum(data) / len(data)


# standard deviation of sample
def calculate_standard_deviation(data):
  return stats.tstd(data)

def calculate_z_score(data):
  return stats.zscore(data)


# milage distribution
# ***************************************************************
def calc_milage_to_maintance(z_score):
  # we are assuming a few things here.
  # Primarily that 98% of cars on the road have travelled between 20000 and 80000 units (km or miles)
  return 50000 + (z_score * 12931.0344)



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
    return [filter_dict_by_param(point, params) for point in data]

  if group_by not in params:
    print("The chosen aggregate value groub_by` must be in the filtered list `params`")
    return False

  return {group_by: [filter_dict_by_param(point, params)[group_by] for point in data]}


# This assumes a dictionary with one single key.
# If a multikey dictionary is passed in, it will return the value of the first key
def get_dict_val(dictionary):
  key = [key for key in dictionary.keys()][0]
  return dictionary[key]


