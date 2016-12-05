The pacakgetest modules allows you to build and tests kolabclient for different distros.

# Usage

First you create the image you want to test:

```
testenv.py build packagetest [distro]
```

it will show you the possible distros (the name of the subdirs). f.ex. ubuntu1604.

After creating the docker image you can run it:

```
testenv.py packagetest [distro]
```
