#!/bin/bash

# Example showing how to start a shell running inside a Singularity container.
#
# The "--bind hostdir:containerdir" option can be used to bind host directories to the container, for example:
#
#     singularity shell --bind /foo:/foo --bind /bar:/bar atse-astra-1.2.4.simg
#
# By default, Singularity will bind the calling users home directory to /home/username

singularity shell atse-astra-1.2.4.simg
