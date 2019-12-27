import json


def _open_file(file_path, mode, cb):
  with open(file_path, mode) as file_pointer:
    return cb(file_pointer)


# write to file
def write_to_file(file_path, cb, overwrite=True):
  permission = "w" if overwrite else "a"
  _open_file(file_path, permission, lambda _file: cb(_file))


def read_from_file(file_path, cb):
  return _open_file(file_path, "r", lambda _file: cb(_file))


# useful implementation to read from a json file
def read_json_file(file_path):
  return read_from_file(
      file_path,
      lambda _file: json.load(_file)
  )


# useful implementation to wrtie a json file
def write_json_file(file_path, data):
  write_to_file(
      file_path,
      lambda _file: json.dump(data, _file)
  )
