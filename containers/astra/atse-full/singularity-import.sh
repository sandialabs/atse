#!/bin/bash

# Example showing how to import a Docker container from a GitLab Container Registry to Singularity.
# The output is a single file representing the Singularity image, in this case "atse-astra-1.2.4.simg"

singularity build --docker-login atse-astra-1.2.4.simg docker://atse.sandia.gov:3434/atse/astra:1.2.4
