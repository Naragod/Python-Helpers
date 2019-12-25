import string
import random as rn
import json

# example:
#
# output = [
#   {
#     vin: "2DGHS45TS3GH3",
#     dissipation_value: 0.0345
#     trip_milage: 53,
#     rtc_time_start: 1503521399,
#     rtc_time_end: 1503521400
#   },
#   {
#     vin: "2DGHS45TS3GH3",
#     dissipation_value: 0.0345
#     trip_milage: 53,
#     rtc_time_start: 1503521399,
#     rtc_time_end: 1503521400
#   }
# ]


# vin_size=17
vin_size = 2


def generate_random_val(t_range):
  return rn.randint(0, t_range)


def generate_time():
  base = 1503500000
  t_range = 200
  return base + generate_random_val(t_range)


def generate_vin(size=vin_size):
  return ''.join(rn.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def generate_entry():
  start_time = generate_time()
  return {
      "vin": generate_vin(),
      "dissipation_value": generate_random_val(100),
      "trip_milage": generate_random_val(100),
      "rtc_time_start": start_time,
      "rtc_time_end": start_time + generate_random_val(10)
  }


def generate_data(size, result=[]):
  if(size == 0):
    return result

  result.append(generate_entry())
  return generate_data(size - 1, result)


# get energy/km dissipated for all data points
# if the trip milage is 0, set it to 1. This will need to be changed
def set_energy_per_milage(data):
  for d in data:
    if d["trip_milage"] == 0:
      d["trip_milage"] = 1
    e_per_k = d["dissipation_value"] / d["trip_milage"]
    d["e_per_k"] = round(e_per_k, 4)
  return data
