import os
from . import log, util

def patch_package(package, opt):
  patches = f"{opt['patches']}/{package['name']}"
  # just so that execute_command doesn't die,
  # define the build_dir key temporarily
  package["build_dir"] = None

  if os.path.isdir(patches):
    log.patching(package["name"])
    for patch in os.listdir(patches):
      # apply patches
      cwd = os.getcwd()
      os.chdir(f"{util.get_package_directory(package, opt)}/..")
      util.execute_command(
        package, ["patch", "-p0", "<", f"{patches}/{patch}"], opt)
      os.chdir(cwd)
