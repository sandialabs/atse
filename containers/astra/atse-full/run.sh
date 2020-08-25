#!/bin/bash

# The SYS_PTRACE capability is needed to enable ptrace
# If you want to open everything up, add '--security-opt seccomp:unconfined' option to the docker run command.
docker run -ti --rm --cap-add SYS_PTRACE atse.sandia.gov:3434/atse/astra:1.2.4
