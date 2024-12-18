import io
import os
import json
import subprocess
import urllib.request

from colored import fg, attr

from . import fetch, log, build, patch, util
from .dependencies import DependencyGraph

known_options = [
  "name",
  "git",
  "ftp",
  "tag",
  "build",
  "clone-at",
  "separate",
  "dependencies"
]

def ordinal(n):
  return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) *
                                  (n % 10 < 4) * n % 10::4])

def check_package(p):
  if type(p) is not dict:
    log.error("packages.yml in invalid.")
    exit(1)

  for opt in p.keys():
    if (opt not in known_options) and (opt != "build"):
      return False
  return (("name" in p) and (("git" in p) ^ ("ftp" in p)))

def dump_to_cache(d, cache):
  cache.seek(0)
  json.dump(d, cache)
  cache.truncate()

def install_packages(packages, args, opt):
  order = []
  packages_dict = {}

  # convert list of packages to dictionary
  for i, package in enumerate(packages):
    if not check_package(package):
      try:
        log.error(
            f"couldn't parse package {package['name']}."
        )
      # hack to catch unnamed packages early
      except KeyError:
          log.error(
            f"{ordinal(i+1)} package has no name."
          )
      return

    # while we're at it, we save the package's source directory
    package["source_dir"] = util.get_package_directory(package, opt)
    packages_dict[package["name"]] = package

  # set correct installation order
  deps = DependencyGraph(packages_dict)
  order = deps.resolve_dependencies()
  if args["list"]:
    log.println("packages will be installed in the following order:")
    for package in order:
      log.println(f" - {attr('bold')}{fg('green')}{package['name']}{attr('reset')}")
    return

  # clone/retrieve source code for each package
  if args["build"]:
    # attempt to read cache
    already_installed = {}
    with open(f"{opt['working-dir']}/.cache", 'a+') as cache:
      cache.seek(0)
      try:
        already_installed = json.load(cache)
      except json.decoder.JSONDecodeError:
        # cache is empty
        pass

      # try to install packages
      # note: we open the file again, since opening it as 'r+' at the beginning
      # would mess things up
      with open(f"{opt['working-dir']}/.cache", 'r+') as cache:
        for package in order:
          name = package["name"]
          if name not in already_installed:
            log.fetching(name)
            fetch.get_source(package, opt)
            # patch package
            if opt["patches"] != None:
              patch.patch_package(package, opt)
          else:
            continue

          # write new packages to cache
          already_installed[name] = "installed"
          dump_to_cache(already_installed, cache)

        # build packages
        for package in order:
          name = package["name"]
          if name in already_installed:
            if already_installed[name] != "built":
              if build.install_package(package, opt):
                already_installed[name] = "built"
                dump_to_cache(already_installed, cache)
            else:
                log.skipping(name)
