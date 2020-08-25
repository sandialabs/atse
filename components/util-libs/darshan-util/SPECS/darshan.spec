
#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname darshan-util

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_UTILS}/darshan-util/%{version}

Summary:   Utilities to process logs from darshan-runtime
Name:      %{pname}%{PROJ_DELIM}
Version:   3.1.8
Release:   1%{?dist}
License:   MIT
Group:     %{PROJ_NAME}/util-libs
URL:       http://www.mcs.anl.gov/research/projects/darshan/
Source0:   darshan-%{version}.tar.gz
Patch0:    darshan-pkgconfig-path.diff

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
%patch0

%build

# override with newer config.guess for aarch64
%ifarch aarch64 || ppc64le
cp /usr/lib/rpm/config.guess bin
%endif

cd darshan-util
./configure --prefix=%{install_path} || { cat config.log && exit 1; }

make %{?_smp_mflags} V=1

# Make sure make check passes
#make %{?_smp_mflags} check

%install

export NO_BRP_CHECK_RPATH=true

cd darshan-util
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT V=1 install

# OpenHPC module file
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{PNAME} library and executables."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{PNAME}"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set     version			    %{version}

depends-on zlib

prepend-path    PATH                %{install_path}/bin
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          DARSHAN_UTIL_DIR        %{install_path}
setenv          DARSHAN_UTIL_BIN        %{install_path}/bin
setenv          DARSHAN_UTIL_LIB        %{install_path}/lib

family "darshan_util"

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}
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

