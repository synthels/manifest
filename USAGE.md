# Usage

Create a file named `packages.yml` in the root directory
of your project. Let it begin like so:

```yaml
build:
  sysroot: sysroot
  working-dir: working
  prefix: prefix
  patches: patches
```

## sysroot

For builds requiring a sysroot (gcc for example), you can define one using

```yaml
sysroot: path/to/sysroot
```

This will work just fine and the sysroot will be created if it doesn't already exist. If you need multiple nested subdirectories within the sysroot, you can also pass a list of paths.

```yaml
sysroot:
  - path/to/sysroot
  - subdir1/subdir1
  - subdir2/subdir2/subdir3
```

In this case, the first path in the list will be treated as the sysroot and every other directory will be created relative to this one.

## The other header options

- `working-dir` is the directory where all of the built packages and their sources will go.
- `prefix` is the directory relative to `working-dir` where your binaries will be installed.
- `patches` is the directory relative to `working-dir` where patches for each package can be found. Patches for each package are expected to be laid out under directories of the form `<patches>/package_name`.

The default values for these fields are as follows:
```py
{
  "sysroot": "sysroot", 
  "working-dir": ".manifest", 
  "prefix": "bin",
  "patches": None
}
```

## Packages

Under the `build` header is where you lay out your packages.

```yaml
packages:
  - name: name # Package name
    # Options...
```

The options for each package are as follows:

- `git`: If the source is hosted on a git repository, this field specifies the URL to that repository.
- `ftp`: If the source is hosted on an FTP server, this field specifies the URL to the source. (Extepcted to be a `gz` or `xz` file).
- `tag`: If `git` is set, this is the tag which will be cloned.
- `clone-at`: Where the source will be cloned (applies both to `git` and `ftp`).
- `recursive`: If `git` is set, clones submodules.
- `separate`: If set, the package's source and build directories will be separated.

## Dependencies

Under any one package, you may list a number of other packages which must be built and available for this one. You do this, as expected, like so:

```yaml
dependencies:
  - package1
  - package2
  # ...
```

## Building packages

The build process happens in three steps. `configure`, `compile` and `install`. The arguments for each step can be configured under the `build` option for each package.

```yaml
build:
  configure:
    - ['some-command', 'and-arguments', 'more-arguments']
    - ['another-command', 'MORE-ARGUMENTS']
  compile:
    - ['make', '-j%CORES']
  install:
    - ['make', 'install']
```

In every command that is ran, you can expect that the current directory will be set to wherever the current package's source was installed (unless the `separate` option was set, in which case the current directory will be set to the package's build directory). In these commands, you can also use a set of special variables, which you prefix with `%`. These variables are the following.

- `%CORES`: Number of CPU cores available in the system.
- `%PREFIX`: The prefix set in the header.
- `%SYSROOT`: The sysroot set in the header.
- `%PROJECT_SOURCE_DIR`: The directory where `manifest` was called from.
- `%THIS_DIR`: Points to the current package's source directory
- `%BUILD_DIR`: Points to the current package's build directory. (if it exists, otherwise points to the same value as `%THIS_DIR`)
