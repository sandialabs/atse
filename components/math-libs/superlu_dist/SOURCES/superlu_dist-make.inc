############################################################################
#
#  Program:         SuperLU_DIST
#
#  Module:          make.inc
#
#  Purpose:         Top-level Definitions
#
#  Creation date:   March 1, 2016	version 5.0.0
#
#  Modified:	    January 22, 2019
#		    
#
############################################################################
#
#  The name of the libraries to be created/linked to
#
SuperLUroot	=
DSUPERLULIB   	= $(SuperLUroot)/SRC/libsuperlu_dist.a
INCLUDEDIR   	= $(SuperLUroot)/SRC

BLASDEF		= -DUSE_VENDOR_BLAS
BLASLIB		= -lopenblas

HAVE_PARMETIS   = TRUE
METISLIB        = -L$(METIS_LIB) -lmetis
PARMETISLIB     = -L$(PARMETIS_LIB) -lparmetis
I_PARMETIS      = -I$(PARMETIS_INC) -I$(METIS_INC)

INCLUDES        = -I$(ZLIB_INC) -I$(BZIP2_INC) -I$(METIS_INC) -I$(PARMETIS_INC) -I$(OPENBLAS_INC)
LIBS            = $(DSUPERLULIB) -L$(ZLIB_LIB) -L$(BZIP2_LIB) -L$(METIS_LIB) -L$(PARMETIS_LIB) -L$(OPENBLAS_LIB) -lparmetis -lmetis $(BLASLIB) -lbz2 -lz

#
#  The archiver and the flag(s) to use when building archive (library)
#  If your system has no ranlib, set RANLIB = echo.
#
ARCH         = ar
ARCHFLAGS    = cr
RANLIB       = ranlib

CC           = $(MPICC)
CFLAGS 	     += -O3 -DNDEBUG $(BLASDEF) -DDEBUGlevel=0 -DPRNTlevel=0 $(INCLUDES) -fopenmp -std=c99 -fPIC -DPIC -g
NOOPTS       = -O0
FORTRAN	     = $(MPIF90)

LOADER       = $(CC) -fopenmp
LOADOPTS     = 
