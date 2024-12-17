"""
Usage:
  manifest build
  manifest list

Options:
  -h --help     Show this message
"""

import os
import shutil

import yaml
import pathlib

from docopt import docopt

from manifest.core import install, log, util

__version__ = "1.0.0"

requirements = ["git", "make", "patch"]

def require(req):
  for r in req:
    if shutil.which(r) == None:
      log.error(
        f"{r} is required for manifest to function."
      )

def is_null_list(x):
  if type(x) is list:
    return x == [None] * len(x)
  return False

def check_any_empty(x):
  """
  check whether
  a yaml contains any null entries.
  """
  if type(x) is dict:
    for key in x:
      a = x[key]
      if a is None or is_null_list(a):
        log.error(f"option \"{key}\" is empty.")
        exit(1)
      check_any_empty(a)
  elif type(x) is list:
    for a in x:
      check_any_empty(a)

def parse_sysroot(opt):
  if opt is None:
    log.error("no directories found under sysroot")
    exit(1)

  # hack alert!
  # we handle this separately, in order to support both the
  # sysroot: 'str' syntax and the tree-like syntax
  if isinstance(opt, str):
    util.mkdir(opt)
    return str(pathlib.Path(opt).absolute())

  # create subdirectories
  base = str(pathlib.Path(opt[0]).absolute())
  try:
    util.mkdir(base)
    for i in opt[1:]:
      util.mkdir(os.path.join(base, i))
    return base
  except OSError as e:
    log.error(f"couldn't create sysroot: ({e})")
    exit(1)

  return base

def get_build_options(yml):
  build_options = {
    "sysroot": "sysroot", 
    "working-dir": ".manifest", "prefix": "bin",
    "patches": None, 
    "project_dir": str(pathlib.Path(os.getcwd()).absolute())
  }

  for key, val in yml.items():
    if key == "build":
      for opt, v in val.items():
        try:
          if opt in ["prefix", "patches"]:
            v = str(pathlib.Path(v).absolute())
          # parse sysroot options
          elif opt == "sysroot":
            v = parse_sysroot(v)
          build_options[opt] = v
        except TypeError:
          # hacky, but gets the job done
          log.error(f"couldn't parse {opt}.")
          exit(1) # return prints a stacktrace. Why am I
                  # still allowed to write python?
  return build_options

def configure_working_directory(opt):
    util.mkdir(opt["working-dir"])

def main():
  args = docopt(__doc__)
  log.bold(f"manifest v{__version__}")
  try:
    with open("packages.yml", "r") as f:
      try:
        y = yaml.safe_load(f)
        require(requirements)
        check_any_empty(y)
        build_options = get_build_options(y)
        configure_working_directory(build_options)
        if "packages" not in y:
          log.error("no packages found in packages.yml.")
        for key, val in y.items():
          # actually install packages
          if key == "packages":
            install.install_packages(val, args, build_options)
      except yaml.YAMLError as exc:
        log.error(exc)
        return
  except FileNotFoundError:
    log.error("packages.yml not found in current directory.")
    pass


if __name__ == "__main__":
    main()
