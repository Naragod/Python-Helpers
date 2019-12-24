# from connector import connector
import dataManipulation as dMan
import dataGenerator as dGen

# alias
# ***************************************************************
get_val = dMan.get_dict_val

# set data
# ***************************************************************
data = dGen.generate_data(10)
data = dGen.set_energy_per_milage(data)

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


# print(data)
# print(trip_milage)
# print(dissipation_value)
print(e_per_k)

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
