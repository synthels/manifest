import os
import pathlib
import subprocess

from . import log, util

def create_build_directory(package, opt):
  clone_at = ""
  if "clone-at" in package:
      clone_at = package["clone-at"]
  path = os.path.join(opt["working-dir"], clone_at, "build", package["name"])
  util.mkdir(path)
  return str(pathlib.Path(path).absolute())

def install_package(package, opt):
  name = package["name"]
  if "build" in package:
    build = package["build"]
    try:
      stages = {
        "configure": "configuring",
        "compile": "compiling",
        "install": "installing"
      }

      # we change our directory to the directory
      # where the installed package resides
      cwd = os.getcwd()
      build_dir = util.get_package_directory(package, opt)
      log.info(f"BUILDDIR: {build_dir}")
      package["build_dir"] = build_dir
      if "separate" in package:
        if package["separate"]:
          dirloc = create_build_directory(package, opt)
          build_dir, package["build_dir"] = [dirloc] * 2

      os.chdir(build_dir)
      for stage in stages:
        if stage in build:
          log.info(f"{stages[stage]} {name}...")
          for args in build[stage]:
            util.execute_command(package, args, opt)
      # go back to root
      os.chdir(cwd)

    # maybe a bit too generic for this, but it gets the job done
    except Exception as e:
      log.error(f"an exception occurred during installing {name}: {e}")
      exit(1)

  return ("build" in package)
