# from connector import connector
import dataGenerator as dGen
import ioOperators as io
import os.path as path
import json

# variables
# ***************************************************************
file_path = "test_data/__test__.json"

# generate data
# ***************************************************************
def _generate_data(size):
  data = dGen.generate_data(size)
  data = dGen.set_energy_per_milage(data)
  return data

# write to file
# ***************************************************************
def _run_(file_path=file_path, size=10):
  if path.isfile(file_path):
    return

  data = _generate_data(size)
  io.write_to_file(file_path, lambda _file: json.dump(data, _file), True)
  print("File {0} written.".format(file_path))

