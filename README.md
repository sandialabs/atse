# ATSE: Advanced Tri-lab Software Environment

This project contains the build recipes and associated scripts used to create
the ATSE packages used on Astra and its associated testbeds. These recipes are
based on OpenHPC (https://openhpc.community/) with modifications to meet the
unique requirements of Astra, including extended support for Arm compilers,
HPE-MPI, and microarchitecture optimizations.

Building this version of ATSE requires a properly configured Open Build Service
(https://openbuildservice.org/) server. Configuring OBS is complicated and
beyond the scope of this README. The scripts/obs-build-atse-proj.py script is
provided as an example of how to bootstrap a new OBS ATSE project using the
package recipes in this project.
