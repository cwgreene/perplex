# Perplex (ppex)
Command line utility for resolving values of system constants.

# Usage
```
$ ppex -v AF_UNIX             # specfiy variables
AF_UNIX=1
$ ppex -v O_RDONLY -v AF_UNIX # specify multiple variables
O_RDONLY=0
AF_UNIX=1
$ ppex -i ./bob.h -v CHICKEN  # specify additional include and variable
CHICKEN=5
```

Note, by default, if an additional header does not use explicit relative
path or absolute path notation ("./", "../", "/"), it will be assumed to
be a system path.

# CAUTION
This currently works by directly compiling a simple program and
executing it. Do not use with untrusted inputs, or assume arbitrary
code execution.
