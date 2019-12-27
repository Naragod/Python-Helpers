
import asyncio
import json
import os.path as path
from utils import ioOperators as io
from utils import dataGenerator as dGen


# adds higher directory to python modules path
# allowing for quick and dirty import
import sys
sys.path.append("..")


# from connector import connector
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


# mock streaming data
# ***************************************************************
async def stream_data():
  data = generate_data(10)
  io.write_to_file(file_path, lambda _file: json)
  await asyncio.sleep(5)

