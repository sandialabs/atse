#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname netcdf

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

%define ncdf_so_major 7

Name:           %{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Summary:        C Libraries for the Unidata network Common Data Form
License:        NetCDF
Group:          %{PROJ_NAME}/io-libs
Version:        4.6.3
Release:        1%{?dist}
Url:            http://www.unidata.ucar.edu/software/netcdf/
#Source0:	https://github.com/Unidata/netcdf-c/archive/v%{version}.tar.gz
Source0:        v%{version}.tar.gz
Patch0:         atse.patch

BuildRequires:  curl-devel
BuildRequires:  zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM} >= 1.2.5
Requires:       zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM} >= 1.2.5
BuildRequires:  m4
Requires:       lmod%{PROJ_DELIM} >= 7.6.1
BuildRequires:  phdf5-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:       phdf5-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
BuildRequires:  pnetcdf-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:       pnetcdf-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}

#!BuildIgnore: post-build-checks rpmlint-Factory

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a freely-distributed collection of software libraries
for C, Fortran, C++, and perl that provides an implementation of the
interface.  The NetCDF library also defines a machine-independent
format for representing scientific data.  Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The NetCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

NetCDF data is:

   o Self-Describing: A NetCDF file includes information about the
     data it contains.

   o Network-transparent:  A NetCDF file is represented in a form that
     can be accessed by computers with different ways of storing
     integers, characters, and floating-point numbers.

   o Direct-access:  A small subset of a large dataset may be accessed
     efficiently, without first reading through all the preceding
     data.

   o Appendable:  Data can be appended to a NetCDF dataset along one
     dimension without copying the dataset or redefining its
     structure. The structure of a NetCDF dataset can be changed,
     though this sometimes causes the dataset to be copied.

   o Sharable:  One writer and multiple readers may simultaneously
     access the same NetCDF file.


%prep
%setup -q -n %{pname}-c-%{version}
# %patch0 -p1

%build
# OpenHPC compiler/mpi designation
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib
module load phdf5
module load pnetcdf

export CPPFLAGS="-I$HDF5_INC -I$PNETCDF_INC"
export LDFLAGS="-L$HDF5_LIB -L$PNETCDF_LIB"

export CC=$MPICC
export CXX=$MPICXX
export F77=$MPIF77
export F90=$MPIF90
export FC=$MPIFC

./configure --prefix=%{install_path} \
    --enable-shared \
    --enable-netcdf-4 \
    --enable-pnetcdf \
    --disable-dap \
    --disable-jna \
    --with-pic \
    --disable-doxygen \
    --enable-static || { cat config.log && exit 1; }

# karl@ices.utexas.edu (5/17/18) - switching to serial make to avoid
# problems. Others also reporing error with parallel build.
#
# https://github.com/Unidata/netcdf-c/issues/896
make V=1
#make %{?_smp_mflags}

%install
# OpenHPC compiler/mpi designation
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib
module load phdf5
module load pnetcdf

export CPPFLAGS="-I$HDF5_INC -I$PNETCDF_INC"
export LDFLAGS="-L$HDF5_LIB -L$PNETCDF_LIB"

export CC=$MPICC
export CXX=$MPICXX
export F77=$MPIF77
export F90=$MPIF90
export FC=$MPIFC

make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT V=1 install

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the NetCDF C API built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr " "
puts stderr "Note that this build of NetCDF leverages the HDF I/O library and requires linkage"
puts stderr "against hdf5. Consequently, the phdf5 package is loaded automatically with this module."
puts stderr "A typical compilation step for C applications requiring NetCDF is as follows:"
puts stderr " "
puts stderr "\\\$CC -I\\\$NETCDF_INC app.c -L\\\$NETCDF_LIB -lnetcdf -L\\\$HDF5_LIB -lhdf5"

puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{PNAME} built with %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set             version             %{version}

depends-on zlib
depends-on phdf5
depends-on pnetcdf

prepend-path    PATH                %{install_path}/bin
prepend-path    MANPATH             %{install_path}/share/man
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib

prepend-path    CPATH               %{install_path}/include
prepend-path    FPATH               %{install_path}/include
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_INC        %{install_path}/include

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%{OHPC_PUB}
%doc COPYRIGHT
%doc README.md