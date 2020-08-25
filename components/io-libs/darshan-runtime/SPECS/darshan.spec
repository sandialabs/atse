
#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname darshan-runtime

%define ohpc_uarch_dependent 1
%define ohpc_mpi_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{mpi_family}/%{pname}/%{version}

Summary:   A library to collect I/O statistics
Name:      %{pname}-%{mpi_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   3.1.8
Release:   1%{?dist}
License:   MIT
Group:     %{PROJ_NAME}/io-libs
URL:       http://www.mcs.anl.gov/research/projects/darshan/
Source0:   darshan-%{version}.tar.gz

BuildRequires: gnu7-compilers%{PROJ_DELIM}
BuildRequires: zlib
Requires: zlib

#!BuildIgnore: post-build-checks rpmlint-Factory

%description
Darshan is a scalable HPC I/O characterization tool. Darshan is
designed to capture an accurate picture of application I/O behavior,
including properties such as patterns of access within files, with
minimum overhead.

%prep

%setup -q -n darshan-%{version}

%build

# override with newer config.guess for aarch64
%ifarch aarch64 || ppc64le
cp /usr/lib/rpm/config.guess bin
%endif

# OpenHPC compiler/mpi designation
%ohpc_setup_compiler
%ohpc_setup_optflags

cd darshan-runtime
CC=mpicc ./configure --prefix=%{install_path} \
	--with-mem-align=8 \
	--with-log-path=%{OHPC_DARSHAN_LOGS} \
	--with-jobid-env=SLURM_JOBID || { cat config.log && exit 1; }

make %{?_smp_mflags} V=1

# Make sure make check passes
#make %{?_smp_mflags} check

%install

%ohpc_setup_compiler
%ohpc_setup_optflags
export NO_BRP_CHECK_RPATH=true

cd darshan-runtime
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT V=1 install

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{PNAME} library built with %{mpi_family}."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{PNAME} built with %{mpi_family}."
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set     version			    %{version}

depends-on zlib

prepend-path    PATH                %{install_path}/bin
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib
prepend-path	LD_PRELOAD          %{install_path}/lib/libdarshan.so
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          DARSHAN_RUNTIME_DIR        %{install_path}
setenv          DARSHAN_RUNTIME_BIN        %{install_path}/bin
setenv          DARSHAN_RUNTIME_LIB        %{install_path}/lib

family "darshan"

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{mpi_family}/%{pname}/.version.%{version}
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

%post
if ! [ -d %{OHPC_DARSHAN_LOGS} ]; then
	echo "Please link %{OHPC_DARSHAN_LOGS} to a globally accessible directory. Then, run:"
	echo "%{install_path}/bin/darshan-mk-log-dirs.pl."
fi

