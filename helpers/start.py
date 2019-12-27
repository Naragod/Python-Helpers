# from connector import connector
import asyncio
import os.path as path
from utils import ioOperators as io
from utils import dataGenerator as dGen


# adds higher directory to python modules path
# allowing for quick and dirty import
import sys
sys.path.append("..")


# variables
# ***************************************************************
file_path = "test_data/__test__.json"


# generate data
# ***************************************************************
def _generate_data(size):
  data = dGen.generate_data(size, [])
  data = dGen.set_energy_per_milage(data)
  return data


# write to file
# ***************************************************************
def _init_(file_path=file_path, size=10):
  if path.isfile(file_path):
    return

  data = _generate_data(size)
  io.write_json_file(file_path, data)
  print("File {0} written.".format(file_path))


# mock streaming data
# ***************************************************************
async def stream_data(size, wait_time):
  data = _generate_data(size)

  # it would be good to build a cache here so that I am not
  # reading from the db or in this case from the file on
  # every new data generated
  file_data = io.read_json_file(file_path)
  file_data.extend(data)

  io.write_json_file(file_path, file_data)
  print("Streaming data... New entries added: size={0}".format(len(file_data)))
  await asyncio.sleep(wait_time)
  await stream_data(size, wait_time)
