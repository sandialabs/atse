#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname pnetcdf

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

Summary:   A Parallel NetCDF library (PnetCDF)
Name:      %{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   1.11.1
%global    sonum 1
Release:   1%{?dist}
License:   NetCDF
Group:     %{PROJ_NAME}/io-libs
URL:       http://cucis.ece.northwestern.edu/projects/PnetCDF
#Source0:   https://parallel-netcdf.github.io/Release/pnetcdf-%{version}.tar.gz
Source0:   pnetcdf-%{version}.tar.gz

BuildRequires:  grep
BuildRequires:  m4
BuildRequires:  zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:       zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}

%description
PnetCDF is a high-performance parallel I/O library for accessing files in format compatibility with
Unidata's NetCDF, specifically the formats of CDF-1, 2, and 5. The CDF-5 file format, an extension of
CDF-2, supports unsigned data types and uses 64-bit integers to allow users to define large dimensions,
attributes, and variables (> 2B array elements).

%prep

%setup -q -n pnetcdf-%{version}

%build

# override with newer config.guess for aarch64
%ifarch aarch64 || ppc64le
cp /usr/lib/rpm/config.guess scripts
%endif

# OpenHPC compiler/mpi designation
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib

export CC=$MPICC
export CXX=$MPICXX
export F77=$MPIF77
export F90=$MPIF90
export FC=$MPIFC

env
mpicxx -v

./configure --prefix=%{install_path} --enable-static --enable-shared --with-pic || { cat config.log && exit 1; }

%{__make} V=1

%install
# OpenHPC compiler/mpi designation
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib

export CC=$MPICC
export CXX=$MPICXX
export F77=$MPIF77
export F90=$MPIF90
export FC=$MPIFC

%{__make} DESTDIR=$RPM_BUILD_ROOT V=1 install

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set     version                     %{version}

depends-on zlib

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH	    %{install_path}/lib
prepend-path    PKG_CONFIG_PATH     %{install_path}/lib/pkgconfig
prepend-path    MANPATH             %{install_path}/share/man

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

%{__mkdir_p} $RPM_BUILD_ROOT/%{_docdir}

%files
%{OHPC_PUB}
%doc AUTHORS ChangeLog COPYRIGHT CREDITS INSTALL NEWS README RELEASE_NOTES 
