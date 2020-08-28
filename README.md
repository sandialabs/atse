# ATSE: Advanced Tri-lab Software Environment

This project contains the build recipes and associated scripts used to create
the [ATSE](https://vanguard.sandia.gov/ATSE) used on the [Astra Supercomputer](https://vanguard.sandia.gov/index.html) and its associated testbeds. These recipes are initially
based on OpenHPC (https://openhpc.community/). However, ATSE also includes many modifications to meet the
unique requirements of Astra, including extended support for Arm compilers,
HPE-MPI, and micro-architecture optimizations.

ATSE is distributed under an [Apache 2.0 License](LICENSE) with approval from Sandia National Laboratories

The ATSE stack has undergone significant improvements prior to public release.  Please review the [CHANGE LOG](CHANGELOG) for more details.

## Building ATSE packages

Building this version of ATSE requires a properly configured Open Build Service
(https://openbuildservice.org/) server. Configuring OBS is complicated and
beyond the scope of this initial README. The [OBS ATSE script](scripts/obs-build-atse-proj.py) is
provided as an example of how to bootstrap a new OBS ATSE project using the
package recipes in this project.


## ATSE Containers

For more information regarding container versions of ATSE, please reference the associated Astra [README](containers/astra/README.md) for more information.

## SC20

The environment conditions were gathered on an open machine with similar hardware to Astra using the SC20 Author Kit's environment collection script. (https://github.com/SC-Tech-Program/Author-Kit). The results are in (mayer_environment_output.txt). 
