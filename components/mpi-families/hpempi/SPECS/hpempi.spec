%define pname hpempi

%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define hpempi_install_path         /opt/hpe/hpc/hmpt/hmpt-%{version}
%define fortran_module_install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

%if "%{compiler_family}" == "gnu7"
%define c_compiler    gcc
%define cxx_compiler  g++
%define ftn_compiler  gfortran
%endif

%if "%{compiler_family}" == "gnu8"
%define c_compiler    gcc
%define cxx_compiler  g++
%define ftn_compiler  gfortran
%endif

%if "%{compiler_family}" == "arm"
%define c_compiler    armclang
%define cxx_compiler  armclang++
%define ftn_compiler  armflang
%endif

Summary:   HPE MPI and SHMEM
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   2.20
Release:   1%{?dist}
License:   HPE Proprietary
URL:       https://downloads.linux.hpe.com/SDR/project/mpi/
Group:     %{PROJ_NAME}/mpi-families
Source0:   fortran_module_generator.tar.gz

# HPE's MPI RPM should be providing this, but it isn't. Workaround by providing here.
Provides: libmpi++.so()(64bit)

# Requires vendor provided HPE-MPI libraries (HPE-MPI)
BuildRequires: hpe-build-key
BuildRequires: hpe-mpi-release
BuildRequires: MPInside
BuildRequires: cpuset-utils
BuildRequires: hpe-mpi-docs
#BuildRequires: kmod-numatools
#BuildRequires: kmod-xpmem
BuildRequires: libFFIO
BuildRequires: numatools
BuildRequires: sgi-arraysvcs
BuildRequires: sgi-mpt
BuildRequires: sgi-mpt-hmpt
BuildRequires: sgi-mpt-shmem
BuildRequires: sgi-mpt-shmem-hmpt
BuildRequires: sgi-procset
BuildRequires: xpmem

Requires: hpe-build-key
Requires: hpe-mpi-release
Requires: MPInside
Requires: cpuset-utils
Requires: hpe-mpi-docs
#Requires: kmod-numatools
#Requires: kmod-xpmem
Requires: libFFIO
Requires: numatools
Requires: sgi-arraysvcs
Requires: sgi-mpt
Requires: sgi-mpt-hmpt
Requires: sgi-mpt-shmem
Requires: sgi-mpt-shmem-hmpt
Requires: sgi-procset
Requires: xpmem

%description
HPE's implementation of the MPI and SHMEM communication APIs.

%prep
%setup -n fortran_module_generator

%build
%ohpc_setup_compiler
%ohpc_setup_optflags

module use /usr/share/Modules/modulefiles
module load hmpt

make %{?_smp_mflags}

%install
%ohpc_setup_compiler
%ohpc_setup_optflags

module use /usr/share/Modules/modulefiles
module load hmpt

make %{?_smp_mflags} DESTDIR=%{buildroot}/%{fortran_module_install_path} install

# modulefile

%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads HPE MPI and SHMEM built for the %{compiler_family} toolchain."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: HPE MPI and SHMEM built for the  %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: communication libraries"
module-whatis "Description: %{summary}"

set             version                 %{version}

# BEGIN: Standard OpenHPC environment variables
prepend-path    PATH                    %{hpempi_install_path}/bin
prepend-path    LD_LIBRARY_PATH         %{hpempi_install_path}/lib
prepend-path    MANPATH                 %{hpempi_install_path}/man
prepend-path    MODULEPATH              %{OHPC_MODULEDEPS}/%{compiler_family}-%{pname}
prepend-path    MODULEPATH              %{OHPC_MODULEDEPS}/%{pname}

setenv          MPI_DIR                 %{hpempi_install_path}

setenv          %{PNAME}_DIR            %{hpempi_install_path}
setenv          %{PNAME}_BIN            %{hpempi_install_path}/bin
setenv          %{PNAME}_INC            %{hpempi_install_path}/include
setenv          %{PNAME}_LIB            %{hpempi_install_path}/lib

setenv          MPICC                   mpicc
setenv          MPICXX                  mpicxx
setenv          MPIFC                   mpif08
setenv          MPIF77                  mpif77
setenv          MPIF90                  mpif90

# END: Standard OpenHPC environment variables

# BEGIN: Additional environment variables set by HPE's "official" module
prepend-path    CPATH                   %{hpempi_install_path}/include
prepend-path    FPATH                   %{hpempi_install_path}/include
prepend-path    LIBRARY_PATH            %{hpempi_install_path}/lib
setenv          MPI_ROOT                %{hpempi_install_path}
setenv          MPT_VERSION             %{version}
# END: Additional environment variables set by HPE's "official" module

# BEGIN: Setup for %{compiler_family} toolchain
setenv          MPICC_CC                %{c_compiler}
setenv          MPICXX_CXX              %{cxx_compiler}
setenv          MPIF08_F08              %{ftn_compiler}
setenv          MPIF90_F90              %{ftn_compiler}
setenv          OSHCC_CC                %{c_compiler}
setenv          OSHCXX_CXX              %{cxx_compiler}
setenv          OSHF90_F90              %{ftn_compiler}
# END: Setup for %{compiler_family} toolchain

# BEGIN: Misc. Configuration

# HPE-MPI supports SLURM's pmi2 implementation
setenv          SLURM_MPI_TYPE          pmi2
setenv          OHPC_MPI_LAUNCHERS      pmi2

# Tell HPE-MPI where to find FORTRAN modules generated for %{compiler_family}, built above
setenv          MPI_CUSTOM_FORTRAN_MODULES_PATH  %{fortran_module_install_path}
prepend-path    LD_LIBRARY_PATH                  %{fortran_module_install_path}

# END: Misc. Configuration

family "MPI"
EOF

#%post
## Fixup issue in HPE-MPI compiler wrappers.
## The need for this will hopefully go away in a future HPE-MPI release.
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/mpicc
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/mpicxx
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/mpif08
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/mpif77
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/mpif90
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/oshcc
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/oshCC
#sed -i 's/\/usr\/lib64\/libcpuset\.so\.1 \/usr\/lib64\/libbitmask\.so\.1/-lcpuset -lbitmask/g' /opt/hpe/hpc/hmpt/hmpt-2.20/bin/oshfort

%files
%{OHPC_PUB}
