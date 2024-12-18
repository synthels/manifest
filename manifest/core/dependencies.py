import collections
import itertools
import json

from . import log

def diff(li1, li2):
  return [i for i in li1 + li2 if i not in li1 or i not in li2]

class DependencyGraph:
  def __init__(self, packages):
    self.packages = packages
    self.check_dependencies()

  def get_by_name(self, name):
    for _n, p in self.packages.items():
      # no reason to check if name field exists
      # at this point.
      if p["name"] == name:
        return p
    return None

  def check_dependencies(self):
    for _n, package in self.packages.items():
      if "dependencies" in package:
        # check for any cross dependencies
        # that would kill us.
        self.check_cross(package)
        for dep in package["dependencies"]:
          if dep not in self.packages:
            log.error(
              f"unknown package {dep}."
            )
            exit(1)
          if package["name"] == dep:
            log.error(f"{dep} depends on itself.")
            exit(1)

  def check_cross(self, package):
    for d in package["dependencies"]:
      other_package = self.get_by_name(d)
      if "dependencies" in other_package:
        if package["name"] in other_package["dependencies"]:
          log.error(f"{package['name']} and {other_package['name']} depend on eachother.")
          exit(1)

  def resolve_single(self, package):
    for name, dep in self.packages.items():
      if "dependencies" in package:
        if (name in package["dependencies"]) and (not name in self.already_resolved):
          self.resolve_single(dep)
          self.path.append(dep)
          self.already_resolved.append(name)

  def resolve_dependencies(self):
    self.already_resolved = []
    self.path = []
    for _n, package in self.packages.items():
      self.resolve_single(package)

    # after this process, the graph sources will remain,
    # so we will resolve them here
    package_list = []
    for _n, package in self.packages.items():
      package_list.append(package)
    self.path.extend(diff(package_list, self.path))
    return self.path
