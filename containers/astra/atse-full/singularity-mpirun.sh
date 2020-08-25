#!/bin/bash

# Example showing how to use mpirun to launch an application running in a Singularity container image.
# This example starts two instances of the Singularity conainer image, with one container instance running on each of two nodes.
# An MPI PingPong benchmark is then run between the two containers.

mpirun -np 2 -npernode 1 singularity exec atse-astra-1.2.4.simg /opt/atse/libs/gnu7/openmpi3/imb/2018.1/bin/IMB-MPI1 PingPong

# Example run on Stria:
# 
# [ktpedre@stln1 singularity]$ salloc -N 2 -t 4:00:00
# salloc: Granted job allocation 17197
#
# [ktpedre@n1 singularity]$ mpirun -np 2 -npernode 1 singularity exec atse-astra-1.2.4.simg /opt/atse/libs/gnu7/openmpi3/imb/2018.1/bin/IMB-MPI1 PingPong
# #------------------------------------------------------------
# #    Intel (R) MPI Benchmarks 2018 Update 1, MPI-1 part    
# #------------------------------------------------------------
# # Date                  : Fri Jun 14 13:49:36 2019
# # Machine               : aarch64
# # System                : Linux
# # Release               : 4.14.0-115.6.1.1chaos.ch6a.aarch64
# # Version               : #1 SMP Wed May 29 17:26:49 MDT 2019
# # MPI Version           : 3.1
# # MPI Thread Environment: 
# 
# 
# # Calling sequence was: 
# 
# # /opt/atse/libs/gnu7/openmpi3/imb/2018.1/bin/IMB-MPI1 PingPong
# 
# # Minimum message length in bytes:   0
# # Maximum message length in bytes:   4194304
# #
# # MPI_Datatype                   :   MPI_BYTE 
# # MPI_Datatype for reductions    :   MPI_FLOAT
# # MPI_Op                         :   MPI_SUM  
# #
# #
# 
# # List of Benchmarks to run:
# 
# # PingPong
# 
# #---------------------------------------------------
# # Benchmarking PingPong 
# # #processes = 2 
# #---------------------------------------------------
#        #bytes #repetitions      t[usec]   Mbytes/sec
#             0         1000         1.45         0.00
#             1         1000         1.46         0.68
#             2         1000         1.46         1.37
#             4         1000         1.49         2.69
#             8         1000         1.46         5.46
#            16         1000         1.49        10.74
#            32         1000         1.53        20.87
#            64         1000         1.68        38.19
#           128         1000         1.74        73.61
#           256         1000         7.35        34.85
#           512         1000        12.42        41.21
#          1024         1000        24.01        42.65
#          2048         1000         3.82       536.66
#          4096         1000         5.30       772.48
#          8192         1000         8.48       966.44
#         16384         1000        10.91      1501.79
#         32768         1000        14.62      2240.55
#         65536          640        22.45      2919.03
#        131072          320        36.68      3573.84
#        262144          160        53.16      4931.61
#        524288           80        92.02      5697.85
#       1048576           40       169.28      6194.40
#       2097152           20       330.15      6352.05
#       4194304           10       653.76      6415.63
#
#
# # All processes entering MPI_Finalize
