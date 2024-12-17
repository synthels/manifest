# manifest

describe your package and dependencies with yaml.

## Installation

```bash
# clone the repo
$ git clone https://github.com/synthels/manifest.git

# change your working directory
$ cd manifest

# install globally
$ python3 -m pip install .

# You can then invoke manifest anywhere!
$ python3 -m manifest
```

## Basic usage

`manifest` works by parsing a simple YAML file (named `packages.yml`), where you describe your packages and their dependencies. The skeleton of this file consists of:

```yaml
build:
  sysroot: "sysroot" # System root
  working-dir: "working_dir" # Build working directory
  prefix: "prefix" # Binary prefix
  patches: "patches_dir" # Directory where patches can be found

packages:
  # Packages go here
```

Under `packages`, you may list any number of packages you want to install, like this:

```yaml
- name: name # Package name
  clone-at: directory # Where the package will be cloned (relative to build/working-dir)
  git: 'git://sourceware.org/git/binutils-gdb.git' # Git repository (if the source is hosted on git)
  ftp: 'https://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz' # ftp url (if the source is hosted on some random server on the internet)
  tag: 'binutils-2_32' # Git tag (applies only if source is hosted on git)
  dependencies: # Packages which need to be built before this package
      - package1
      - package2
  build:
    # Build options (see USAGE.md)
```

The subcommands are as follows:

```sh
$ python3 manifest.py --help

Usage:
  manifest build    Build packages
  manifest list     List packages

Options:
  -h --help     Show this message
```

For more details, see [`USAGE.md`](https://github.com/synthels/manifest/blob/master/USAGE.md).
