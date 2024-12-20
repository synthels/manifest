# manifest

Create portable distributions for your packages the easy way.

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

`manifest` works by parsing a YAML file (called `packages.yml`), where you describe your package, subpackages and their dependencies. The file looks like this:

```yaml
build:
  sysroot: "sysroot"
  working-dir: "working_dir"
  prefix: "prefix"
  patches: "patches_dir"

packages:
  # ...
```

Under `packages`, you may list any number of packages you want to install, like this:

```yaml
- name: name
  clone-at: directory
  git: repo
  ftp: url
  tag: tag
  dependencies:
      - package1
      - package2
      - # ...
  build:
    # ...
```

The subcommands are as follows:

```sh
$ python3 manifest.py --help

Usage:
  manifest build    Build packages
  manifest list     List packages

Options:
  -h --help         Show this message
```

For more details, see [USAGE](https://github.com/synthels/manifest/blob/master/USAGE.md).
