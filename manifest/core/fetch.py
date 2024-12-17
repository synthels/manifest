import os
import subprocess
import urllib.request, urllib.error
import tarfile

from . import log

def from_git(package, clone_at):
  if "tag" in package:
      repo = ("--depth", "1", "--branch", f"{package['tag']}",
        f"{package['git']}")
  else:
      repo = ("--depth", "1", package["git"])

  command = ["git", "clone", *repo, f"{clone_at}/{package['name']}"]
  if "recursive" in package:
    command.append("--recursive")

  p = subprocess.run(
    command,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)

  # did we actually clone anything?
  if p.returncode != 0:
    log.error(
      f"couldn't clone {package['git']}. (git exit code: {p.returncode})")
    exit(1)

def from_ftp(package, clone_at):
  # urlretrieve complains if the directory we give
  # it doesn't exist...
  cloned_at = f"{clone_at}/{package['name']}"
  if not os.path.isdir(clone_at):
    os.makedirs(clone_at)

  try:
    urllib.request.urlretrieve(package["ftp"], f"{cloned_at}.tar.gz")
  except urllib.error.URLError:
    log.error(f"couldn't resolve {package['ftp']}.")
    exit(1)

  # we assume (WLOG) that the file is a tarball
  tar = tarfile.open(f"{cloned_at}.tar.gz", "r:gz")
  tar.extractall(path=clone_at)
  extracted = os.path.commonprefix(tar.getnames())
  tar.close()

  # remove tar file and rename extracted archive to package name
  os.remove(f"{cloned_at}.tar.gz")
  os.rename(f"{clone_at}/{extracted}", f"{clone_at}/{package['name']}")


def get_source(package, opt):
  clone_at = opt['working-dir']
  if "clone-at" in package:
    clone_at = f"{clone_at}/{package['clone-at']}"

  if os.path.isdir(f"{clone_at}/{package['name']}"):
    log.error(f"the previous build probably failed and you're running it again; please delete the build directory first.")
    exit(1)

  if "git" in package:
    from_git(package, clone_at)
  elif "ftp" in package:
    from_ftp(package, clone_at)
