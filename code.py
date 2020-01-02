from connector import connector
from utils import dataManipulation as dMan
from utils import dataGenerator as dGen
from utils import ioOperators as io


# variables
# ***************************************************************
config_path = "config.json"
config = io.read_json_file(config_path)
file_path = config["file_path"]
dbConfig = io.read_json_file("connector/config.json")["local"]
conn = connector.Connector(dbConfig)

# alias
# ***************************************************************
get_val = dMan.get_dict_val


# obtain data
# ***************************************************************
# obtain data from db
def insert_to_table(connection, data, table_name):
  for obj in data:
    keys_arr = list(obj.keys())
    keys = ','.join(x for x in keys_arr)
    values_arr = list(obj.values())
    values = ','.join("'" + x + "'" if isinstance(x, str)
                      else str(x) for x in values_arr)
    query = "insert into {0} ({1}) values({2})".format(
        table_name, keys, values)
    print(query)
    connection.query(query)


def read_from_table(connection, table_name):
  query = "select * from {0}".format(table_name)
  return connection.query(query)


data = read_from_table(conn, "test_table")

# logic
# ***************************************************************
filtered_list = dMan.filter_list_by_param(
    data,
    [
        "vin",
        "dissipation_value",
        "trip_mileage",
        "e_per_k"
    ]
)

f_data = dMan.aggregate_values(filtered_list, "vin", [])
e_per_k = dMan.filter_list_by_param(
    f_data,
    ["vin", "e_per_k"],
    "e_per_k",
    True
)

e_per_k_zscores = dMan.calculate_z_score(get_val(e_per_k))
mileages = dMan.calc_all_mileages_to_maintenance(e_per_k_zscores)

# append z_scores and mileage_to_maintenance to the data
dMan.append_prop_to_objs(f_data, "z_score", get_val(e_per_k))
dMan.append_prop_to_objs(f_data, "mileage_to_maintenance", mileages)

print(f_data)


# write to db
# ***************************************************************
# keys = [
#     "vin",
#     "date_computed",
#     "z_score",
#     "predicted_brake_job_mileage",
#     "last_known_brake_maintenance_date",
#     "last_known_brake_job_mileage",
#     "cohort_spec",
#     "cohort_hash",
#     "cohort_n",
# ],
# def aaaa():
#   for obj in data:
#     obj["date_computed"] = datetime.datetime.utcnow()
#     dGen.generate_template()
# insert_to_table(conn, computed_data, "brake_model_mileage")
