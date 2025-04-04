import os
import subprocess
import pathlib

def get_cores():
  try:
    cpus = os.sched_getaffinity(0)
  except AttributeError:
    return os.cpu_count()
  return len(cpus)

def parse(commands, package, opt):
  variables = {
    "CORES": str(get_cores()),
    "PREFIX": opt["prefix"],
    "SYSROOT": opt["sysroot"],
    "THIS_DIR": package["source_dir"],
    "BUILD_DIR": package["build_dir"],
    "PROJECT_SOURCE_DIR": opt["project_dir"]
  }

  for i, c in enumerate(commands):
    for s in variables:
      # sometimes, I feel really sad and null-out values
      # that I really shouldn't
      if variables[s] is not None:
        commands[i] = commands[i].replace(f"%{s}", variables[s])
  return commands

def execute_command(package, args, opt):
  parsed = parse(args, package, opt)
  return os.system(" ".join(parsed))

def get_package_cloned_at_directory(package, opt):
  directory = opt["working-dir"]
  if "clone-at" in package:
    directory = f"{directory}/{package['clone-at']}"
  return directory

def get_package_directory(package, opt):
  directory = opt["working-dir"]
  if "clone-at" in package:
    directory = os.path.join(
      directory, package["clone-at"], package["name"]
    )
  return str(pathlib.Path(directory).absolute())

def mkdir(path):
  if not os.path.isdir(path):
    os.makedirs(path)
