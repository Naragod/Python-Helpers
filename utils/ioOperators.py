
def _open_file(file_path, mode, cb):
  with open(file_path, mode) as file_pointer:
    return cb(file_pointer)


# write to file
def write_to_file(file_path, cb, overwrite=False):
  permission = "w" if overwrite else "a"
  _open_file(file_path, permission, lambda _file: cb(_file))


def read_from_file(file_path, cb):
  return _open_file(file_path, "r", lambda _file: cb(_file))
