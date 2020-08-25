#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname mpiP

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%{version}

# Note: this package is slightly non-standard in that we always use
# gnu compilers underneath in order to support call-site demangling
%if "%{compiler_family}" == "intel"
Requires:      intel-compilers-devel%{PROJ_DELIM}
BuildRequires: gnu7-compilers%{PROJ_DELIM}
Requires:      gnu7-compilers%{PROJ_DELIM}
%if "%{mpi_family}" != "impi"
BuildRequires: %{mpi_family}-gnu7%{UARCH_DELIM}%{PROJ_DELIM}
Requires:      %{mpi_family}-gnu7%{UARCH_DELIM}%{PROJ_DELIM}
%endif
%endif

Summary:   mpiP: a lightweight profiling library for MPI applications.
Name:      %{pname}-%{compiler_family}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   3.4.1
Release:   1%{?dist}
License:   BSD-3
Group:     %{PROJ_NAME}/perf-tools
URL:       http://mpip.sourceforge.net/
Source0:   http://sourceforge.net/projects/mpip/files/mpiP/mpiP-3.4.1/mpiP-%{version}.tar.gz
Patch1:    mpip.unwinder.patch

BuildRequires: binutils%{PROJ_DELIM}
BuildRequires: python

# Note: this package is slightly non-standard in that we always use
# gnu compilers underneath in order to support call-site demangling
BuildRequires: gnu7-compilers%{PROJ_DELIM}
Requires:      gnu7-compilers%{PROJ_DELIM}
BuildRequires: %{mpi_family}-gnu7%{UARCH_DELIM}%{PROJ_DELIM}
Requires:      %{mpi_family}-gnu7%{UARCH_DELIM}%{PROJ_DELIM}

%description

mpiP is a lightweight profiling library for MPI applications. Because
it only collects statistical information about MPI functions, mpiP
generates considerably less overhead and much less data than tracing
tools. All the information captured by mpiP is task-local. It only
uses communication during report generation, typically at the end of
the experiment, to merge results from all of the tasks into one output
file.

%prep

%setup -q -n %{pname}-%{version}
%patch1 -p1

%build

# override with newer config.guess for aarch64
%ifarch aarch64 || ppc64le
cp /usr/lib/rpm/config.guess bin
%endif

# OpenHPC compiler/mpi designation

# note: in order to support call-site demangling, we compile mpiP with gnu
module load gnu7
%ohpc_setup_optflags
module load %{mpi_family}

CC=$MPICC
CXX=$MPICXX
FC=$MPIFC

%ifarch aarch64
./configure --prefix=%{install_path} --enable-demangling --disable-libunwind --enable-setjmp || { cat config.log && exit 1; }
%else
./configure --prefix=%{install_path} --enable-demangling --disable-libunwind || { cat config.log && exit 1; }
%endif

%install

# OpenHPC compiler designation

# note: in order to support call-site demangling, we compile mpiP with gnu
module load gnu7
%ohpc_setup_optflags
module load %{mpi_family}

make %{?_smp_mflags} shared
make DESTDIR=$RPM_BUILD_ROOT install

# OpenHPC module file
%{__mkdir} -p %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
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
module-whatis "Category: Profiling library"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set             version             %{version}

prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib

prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_LIB        %{install_path}/lib

EOF

%{__mkdir} -p $RPM_BUILD_ROOT/%{_docdir}

%files
%{OHPC_PUB}
%doc ChangeLog doc/PORTING.txt doc/README doc/UserGuide.txt
