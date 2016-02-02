The kdesrcbuild module allows to build software using kdesrcbuild and other mechanisms. It additionally allows to build using different build environments.

# Environment
The environment to build. This is used to find the kdesrcbuild definition as well as prefix for the source/build and install directory.

# Buildenvironment
The docker image used to build your software. It has all the necessary dependencies installed to build your software and run the tests.

The buildenvironment is stateless as it mounts ~/kdebuild/$ENVIRONMENT under /work/.

# Usage

The srcbuild command is used as follows:
```
testenv.py srcbuild [--buildenv=BUILDENV] ENVIRONMENT COMMAND
```
* BUILDENV: a potential 
* ENVIRONMENT: the environment to use
* COMMAND: one of:
** kdesrcbuild: Run kdesrcbuild
** shell: Open an interactive shell in the container
** $PATH $COMMAND: For everything else PATH is the path to run an arbitrary COMMAND. The PATH is relative to the build directory.


Every environment can in principle be built with every buildenvironment. Typically a buildenvironment is only used with a single environment (i.e. one in fedora and one in debian).
A default buildenvironment is defined for every environment so it is not necessary to specify the buildenvironment normally.

To build i.e. kube:
```
testenv.py srcbuild kube kdesrcbuild
```

This will build kube in the fedora-kube container which is the default buildenvironment for the kube envrionment. To alternatively build it in the fedora-kde buildenvironment:

```
testenv.py srcbuild --buildenv=fedora-kde kube kdesrcbuild
```

To run make install in the kube environment on the sink/common directory:
```
testenv.py srcbuild kube sink/common make install
```

Note that any output that you get from running a custom command or kdesrcbuild (so not from the interactive shell), will have all paths starting with /work (the internal mountpoint of the working directory) replaced with corresponding host paths. This allows for easy interaction with the command line as well as integration with tools that e.g. expect make output (e.g. the vim Make command).

# Directory layout

Using any build environment will result in the following folder hierarchy in your ROOT (~/kdebuild/ by default, see settings.py):
```
~/kdebuild/kube/source/*
~/kdebuild/kube/build/*
~/kdebuild/kube/install/*
```
It is therefore only possible at the moment to build using one buildenvironment at a time (we can change that should it become necessary).

# Preparing a buildenvironment

To build the fedora-kube buildenvironment
```
./testenv.py build kdesrcbuild fedora-kube
```
