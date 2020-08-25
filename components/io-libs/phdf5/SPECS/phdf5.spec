#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname hdf5

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

%define _unpackaged_files_terminate_build 0

Summary:   A general purpose library and file format for storing scientific data
Name:      p%{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   1.10.5
Release:   1%{?dist}
License:   Hierarchical Data Format (HDF) Software Library and Utilities License
Group:     %{PROJ_NAME}/io-libs
URL:       http://www.hdfgroup.org/HDF5

#Source0:   https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/%{pname}-%{version}/src/%{pname}-%{version}.tar.bz2
Source0:   %{pname}-%{version}.tar.bz2
Patch0:    h5cc.patch
Patch1:    h5fc.patch
Patch2:    h5cxx.patch

BuildRequires: zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:      zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}

#!BuildIgnore: post-build-checks rpmlint-Factory

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF5 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF5 files according to your needs.

%prep

%setup -q -n %{pname}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0

# Fix building with gcc8 (this should be a patch)
sed "s/\(.*\)(void) HDF_NO_UBSAN/HDF_NO_UBSAN \1(void)/" -i src/H5detect.c

%build

# override with newer config.guess for aarch64
%ifarch aarch64 || ppc64le
cp /usr/lib/rpm/config.guess bin
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

# Arm HPC compiler fails building hdf5 when thunderx2 optimizations are enabled.
# TODO: remove this once the underlying issue is fixed
%if "%{compiler_family}" == "arm"
export CFLAGS="%ohpc_optflags"
export CXXFLAGS="%ohpc_optflags"
export FFLAGS="%ohpc_optflags"
export FCFLAGS="%ohpc_optflags"
%endif

./configure --prefix=%{install_path} \
	    --with-pic               \
	    --enable-symbols=yes     \
	    --with-zlib=${ZLIB_DIR}  \
	    --enable-fortran         \
	    --enable-static          \
	    --enable-parallel        \
	    --enable-shared          \
	    --enable-fortran2003     || { cat config.log && exit 1; }

%if "%{compiler_family}" == "llvm" || "%{compiler_family}" == "arm"
%{__sed} -i -e 's#wl=""#wl="-Wl,"#g' libtool
%{__sed} -i -e 's#pic_flag=""#pic_flag=" -fPIC -DPIC"#g' libtool
%endif

make %{?_smp_mflags} V=1

%install

# OpenHPC compiler designation
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib

export NO_BRP_CHECK_RPATH=true

make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT V=1 install

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/p%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/p%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the parallel %{pname} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set     version			    %{version}

depends-on zlib

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib

prepend-path    CPATH               %{install_path}/include
prepend-path    FPATH               %{install_path}/include
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include

family "hdf5"
EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/p%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%{OHPC_PUB}
%doc COPYING
%doc README.txt
