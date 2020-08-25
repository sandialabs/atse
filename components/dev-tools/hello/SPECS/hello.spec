#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname hello

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

Summary:   Hello world, prints MPI and OpenMP affinity
Name:      %{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   1.0.0
Release:   1%{?dist}
License:   GPL
Group:     %{PROJ_NAME}/utils
URL:       https://www.sandia.gov
Source0:   %{pname}-%{version}.tar.gz

%description
Hello world program that prints MPI and OpenMP affinity to the console.

%prep
%setup -n %{pname}-%{version}

%build
%ohpc_setup_compiler
%ohpc_setup_optflags

make V=1

%install
%ohpc_setup_compiler
%ohpc_setup_optflags

%{__mkdir} -p %{buildroot}%{install_path}/bin
cp hello  %{buildroot}%{install_path}/bin/.

# OpenHPC module file
%{__mkdir} -p %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} utility built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: utility"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set           version             %{version}

prepend-path  PATH                %{install_path}/bin

EOF

%files
%{OHPC_PUB}
