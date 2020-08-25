#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname parmetis

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

Name:	%{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version: 4.0.3
Release: 1%{?dist}
Summary: Parallel Graph Partitioning and Fill-reducing Matrix Ordering
License: Parmetis License (US Government and Non-profit only)
Group: %{PROJ_NAME}/parallel-libs
URL: http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview
#Source0: http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-%{version}.tar.gz
Source0: parmetis-%{version}.tar.gz

BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: cmake

%description
ParMETIS is an MPI-based parallel library that implements a variety of
algorithms for partitioning unstructured graphs, meshes, and for computing
fill-reducing orderings of sparse matrices. ParMETIS extends the functionality
provided by METIS and includes routines that are especially suited for parallel
AMR computations and large scale numerical simulations. The algorithms
implemented in ParMETIS are based on the parallel multilevel k-way
graph-partitioning, adaptive repartitioning, and parallel multi-constrained
partitioning schemes developed in our lab.  ParMETIS provides five major
functions: graph partitioning, mesh partitioning, graph repartitioning,
partitioning refinement, and matrix reordering.

%prep
%setup -q -n %{pname}-%{version}

%install
%ohpc_setup_compiler
%ohpc_setup_optflags

# Build and install static library
make config prefix=%{install_path}
make V=1
make install DESTDIR=${RPM_BUILD_ROOT}

# Build and install shared library
make clean
make config shared=1 prefix=%{install_path}
make V=1
make install DESTDIR=${RPM_BUILD_ROOT}


# OpenHPC module file
%{__mkdir} -p %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr " "

puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set             version             %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib

prepend-path    CPATH               %{install_path}/include
prepend-path    FPATH               %{install_path}/include
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_INC        %{install_path}/include

family "parmetis"

EOF

%{__mkdir} -p %{buildroot}/%{_docdir}

%files
%{OHPC_PUB}
%doc BUILD.txt Changelog Install.txt LICENSE.txt ./manual/*
