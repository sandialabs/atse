#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname cgns

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

Summary:   CFD General Notation System
Name:      %{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   3.4.0
Release:   1%{?dist}
License:   Zlib
Group:     %{PROJ_NAME}/io-libs
URL:       https://cgns.github.io/download.html

#Source0:   https://github.com/CGNS/CGNS/archive/v%{version}.tar.gz
Source0:   v%{version}.tar.gz
Patch0:    cgns-3.4.0.patch

BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  cmake%{PROJ_DELIM}

BuildRequires:  zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:       zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
BuildRequires:  phdf5-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:       phdf5-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}

%description
The CFD General Notation System (CGNS) provides a general, portable, and
extensible standard for the storage and retrieval of computational fluid
dynamics (CFD) analysis data. It consists of a collection of conventions, and
free and open software implementing those conventions. It is self-descriptive,
machine-independent, well-documented, and administered by an international
steering committee. It is also an American Institute of Aeronautics and
Astronautics (AIAA) Recommended Practice.

%prep

%setup -q -n %{PNAME}-%{version}
%patch0 -p1

%build
%ohpc_setup_compiler
%ohpc_setup_optflags
module load cmake
module load zlib
module load phdf5

mkdir BUILD
cd BUILD

cmake   \
        -D CMAKE_INSTALL_PREFIX=%{install_path} \
        \
        -D CGNS_BUILD_CGNSTOOLS:BOOL=OFF \
        -D CGNS_BUILD_SHARED:BOOL=ON \
        -D CGNS_BUILD_STATIC:BOOL=ON \
        -D CGNS_BUILD_TESTING:BOOL=ON \
        -D CGNS_ENABLE_64BIT:BOOL=ON \
        -D CGNS_ENABLE_BASE_SCOPE:BOOL=ON \
        -D CGNS_ENABLE_FORTRAN:BOOL=ON \
        -D CGNS_ENABLE_HDF5:BOOL=ON \
        -D CGNS_ENABLE_LEGACY:BOOL=ON \
        -D CGNS_ENABLE_MEM_DEBUG:BOOL=OFF \
        -D CGNS_ENABLE_PARALLEL:BOOL=ON \
        -D CGNS_ENABLE_SCOPING:BOOL=ON \
        -D CGNS_ENABLE_TESTS:BOOL=OFF \
        -D CGNS_USE_SHARED:BOOL=ON \
        \
        -D CMAKE_C_COMPILER:STRING=`which $MPICC` \
        -D CMAKE_C_FLAGS_RELEASE:STRING="$CFLAGS -I$HDF5_INC" \
        -D CMAKE_C_FLAGS:STRING="-fPIC -I$HDF5_INC" \
        \
        -D HDF5_DIR=$HDF5_DIR \
        -D HDF5_C_LIBRARY_hdf5:FILEPATH="$HDF5_LIB/libhdf5.a" \
        -D HDF5_NEED_MPI:BOOL=ON \
        -D HDF5_NEED_ZLIB:BOOL=ON \
        \
        -D ZLIB_LIBRARY:FILEPATH=$ZLIB_LIB/libz.a \
        \
        -D CMAKE_EXE_LINKER_FLAGS="-L$HDF5_LIB -ldl" \
        ../

make %{?_smp_mflags} VERBOSE=1
cd ..

%install
%ohpc_setup_compiler
%ohpc_setup_optflags
module load cmake
module load zlib
module load phdf5

cd BUILD
make %{?_smp_mflags} VERBOSE=1 DESTDIR=%{buildroot} install INSTALL='install -p'
cd ..

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the parallel %{pname} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: io library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set             version             %{version}

depends-on zlib
depends-on phdf5

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

EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%{OHPC_PUB}
%doc license.txt
%doc README.md
%doc release_docs/changelog
