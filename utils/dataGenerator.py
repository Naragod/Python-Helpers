import string
import random as rn
import json


# example:
#
# output = [
#   {
#     vin: "2DGHS45TS3GH3",
#     dissipation_value: 0.0345
#     trip_mileage: 53,
#     rtc_time_start: 1503521399,
#     rtc_time_end: 1503521400
#   },
#   {
#     vin: "2DGHS45TS3GH3",
#     dissipation_value: 0.0345
#     trip_mileage: 53,
#     rtc_time_start: 1503521399,
#     rtc_time_end: 1503521400
#   }
# ]


# variables
# ***************************************************************
# vin_size=17
vin_size = 2


# functions
# ***************************************************************
def generate_random_val(t_range):
  return rn.randint(0, t_range)


def generate_time():
  base = 1503500000
  t_range = 200
  return base + generate_random_val(t_range)


def generate_vin(size=vin_size):
  return ''.join(rn.choice(string.ascii_uppercase + string.digits) for _ in range(size))


# The number of keys and values needs to be the same
def generate_template(keys, values, result, index=0):
  if len(keys) != len(values):
    print("Keys and values do not have the same number of items.")
    return result

  if len(keys) == index:
    return result

  key = keys[0]
  value = values[0]
  result[key] = value
  return generate_template(keys, values, result, index + 1)

# this is example specific. Rewrite this function as per data needs


def generate_entry():
  start_time = generate_time()
  keys = [
      "vin",
      "dissipation_value",
      "trip_mileage",
      "rtc_time_start",
      "rtc_time_end"
  ]
  values = [
      generate_vin(),
      generate_random_val(100),
      generate_random_val(100),
      start_time,
      start_time + generate_random_val(10)
  ]
  return generate_template(keys, values, {})


def generate_data(size, result):
  if(size == 0):
    return result

  result.append(generate_entry())
  return generate_data(size - 1, result)


# get energy/km dissipated for all data points
# if the trip mileage is 0, set it to 1. This will need to be changed
def set_energy_per_mileage(data):
  for d in data:
    if d["trip_mileage"] == 0:
      d["trip_mileage"] = 1
    e_per_k = d["dissipation_value"] / d["trip_mileage"]
    d["e_per_k"] = round(e_per_k, 4)
  return data
