# ATSE 1.2.4 for Astra 

This container provides the ATSE software environment version 1.2.4.

## Containers are divided into several separate container images.

Currently ATSE 1.2.4 is only setup to provide the ATSE-Full environment.

If ATSE-GCC7-OPENMPI or ATSE-ARM19-OMPI containers are needed, the Dockerfile
in their respective directory needs updating to be consistent with the
Dockerfile in the atse-full directory.

1. ATSE-Full                - This containers the full ATSE software stack, which includes GCC 7.2 and ARM 20.0 compilers, OpenMPI3, OpenMPI4, and HPE-MPI.
2. [REMOVED] ATSE-GCC7-OMPI  - Container image with only GCC 7.2 compilers and OpenMPI 4 with the related ATSE sotware environment. 
3. [REMOVED] ATSE-ARM19-OMPI - Container image with only the ARM 20.0 compilers and OpenMPI 4 with the related ATSE software environment.

## The ATSE-Full stack has the following software:

* Mellanox OFED 4.7-3.2.9.0 InfiniBand Stack
* Arm 20.0 Compilers
* Arm Allinea Forge 20.0.2 and Reports 20.0.2
* HPE-MPI 1.4
* ATSE 1.2.4 Programming Environment

## General Information

To build each container, cd to the sub-directory andrun build.sh

To run each container using Docker, run run.sh

In the ATSE-Full container images, the container starts bash running as the atse user by default.
Use "sudo su" to become root for anything that requires privilege.

The Arm compilers and tools require a license server to function.  This
container includes the necessary configuration for the Sandia SRN site
license server.  If running on a different network, these license files
need to be updated:

    /opt/arm/licenses/License
    /opt/arm/forge/licenses/License
    /opt/arm/reports/licenses/License

These container images have a few differences compared to native Astra:

* These containers are built from CentOS7, while Astra runs TOSS.
* These containers includes a much smaller set of base OS packages compared to
  Astra. If things are missing, use "yum install packagename" to install.
* The ATSE-Full container is roughly 10 GB, while the Astra image is 30+ GB.
