#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname devpacks

%include %{_sourcedir}/OHPC_macros

Summary:     ATSE Developer Packs
Name:        %{pname}%{PROJ_DELIM}
Version:     20200125
Release:     1%{?dist}
License:     Apache-2.0
URL:         https://atse.sandia.gov
Group:       %{PROJ_NAME}/devpacks

%description
Developer Packs

%install

# GNU7 devpack
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/devpack-gnu7
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/devpack-gnu7/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {
        puts stderr " "
        puts stderr "This module loads the default gnu7 compiler programming environment"
        puts stderr "\nVersion %{version}\n"
}

module-whatis "Name: devpack"
module-whatis "Version: %{version}"
module-whatis "Category: devpack"
module-whatis "Description: This module loads the default gnu7 compiler programming environment"

module load autotools
module load cmake
module load git
module load gnu7
module load zlib
module load bzip2
module load xz
module load yaml-cpp
module load numactl
module load hwloc
module load pmix
module load openucx
module load openmpi4
module load netcdf
module load pnetcdf
module load phdf5
module load cgns
module load parmetis
module load metis
module load openblas
module load superlu
module load superlu_dist
module load boost
module load fftw
module load singularity

family "devpack"
EOF

# ARM devpack
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/devpack-arm
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/devpack-arm/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {
        puts stderr " "
        puts stderr "This module loads the default arm compiler programming environment"
        puts stderr "\nVersion %{version}\n"
}

module-whatis "Name: devpack"
module-whatis "Version: %{version}"
module-whatis "Category: devpack"
module-whatis "Description: This module loads the default arm compiler programming environment"

module load autotools
module load cmake
module load git
module load arm
module load armpl
module load zlib
module load bzip2
module load xz
module load yaml-cpp
module load numactl
module load hwloc
module load pmix
module load openucx
module load openmpi4
module load netcdf
module load pnetcdf
module load phdf5
module load cgns
module load parmetis
module load metis
module load superlu
module load superlu_dist
module load boost
module load fftw
module load singularity

family "devpack"
EOF

%files
%{OHPC_PUB}
