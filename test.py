# from connector import connector
from utils import dataManipulation as dMan
from utils import ioOperators as io
from helpers import start
import asyncio
import json

# variables
# ***************************************************************
file_path = "test_data/__test__.json"
stream_size = 1
initial_data_size = 10
stream_interval = 1


# alias
# ***************************************************************
get_val = dMan.get_dict_val


async def logic():
  while True:
    data = io.read_from_file(
        file_path,
        lambda _file: json.load(_file)
    )
    # print("Beginning search for:{0}".format(
    #     dMan.search_for_all(data, "vin", "F8", [])))

    # manipulate data
    # ***************************************************************
    trip_milage = dMan.filter_list_by_param(
        data,
        ["vin", "trip_milage"],
        "trip_milage",
        True
    )
    dissipation_value = dMan.filter_list_by_param(
        data,
        ["vin", "dissipation_value"],
        "dissipation_value",
        True
    )

    e_per_k = dMan.filter_list_by_param(
        data,
        ["vin", "e_per_k"],
        "e_per_k",
        True
    )

    # print data
    # ***************************************************************

    # search for a specific vin
    # print(dMan.search_for_all(data, "vin", "F8", []))

    # print(data)
    # print(trip_milage)
    # print(dissipation_value)
    # print(e_per_k)
    # e_per_k_mean = dMan.calculate_mean(get_val(e_per_k))
    # e_per_k_deviation = dMan.calculate_standard_deviation(get_val(e_per_k))
    e_per_k_zscores = dMan.calculate_z_score(get_val(e_per_k))
    # print("e_per_k_mean: {0}".format(e_per_k_mean))
    # print("e_per_k_deviation: {0}".format(e_per_k_deviation))
    print("e_per_k_zscoes: {0}".format(e_per_k_zscores))
    # average_milage = dMan.calculate_mean(get_val(trip_milage))
    # deviation_milage = dMan.calculate_standard_deviation(get_val(trip_milage))
    # average_dissipation = dMan.calculate_mean(get_val(dissipation_value))

    # print(type(e_per_k_zscores))

    milages = dMan.calc_all_milages_to_maintance(e_per_k_zscores)
    print("Milages: {0}".format(milages))
    await asyncio.sleep(5)


async def main():
  # Generate Data
  # ***************************************************************
  start._init_(file_path, initial_data_size)

  # begin streaming data
  asyncio.ensure_future(start.stream_data(stream_interval, stream_size))

  await logic()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
