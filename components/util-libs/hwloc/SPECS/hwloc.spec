#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname hwloc

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   Portable hardware affinity library
Name:      %{pname}-%{compiler_family}%{PROJ_DELIM}
Version:   1.11.11
Release:   1%{?dist}
License:   BSD-3-Clause
Group:     %{PROJ_NAME}/libs
URL:       http://www.open-mpi.org/projects/hwloc/
#Source0:   https://www.open-mpi.org/software/hwloc/v1.11/downloads/%{pname}-%{version}.tar.bz2
Source0:   %{pname}-%{version}.tar.bz2

BuildRequires:  doxygen
%if 0%{?sles_version} || 0%{?suse_version}
BuildRequires:  fdupes
%endif
#BuildRequires:  gcc-c++
%if 0%{?suse_version} <= 1220 && !0%{?suse_version}
BuildRequires:  pkgconfig(cairo)
Requires:       pkgconfig(cairo)
BuildRequires:  pkgconfig(libxml-2.0)
Requires:       pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pciaccess)
Requires:       pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)
#Requires:       pkgconfig(x11)
%else
BuildRequires:  cairo-devel
Requires:       cairo
BuildRequires:  libxml2-devel
Requires:       libxml2
BuildRequires:  ncurses-devel
Requires:       ncurses
BuildRequires:  xorg-x11-libICE-devel
#Requires:       xorg-x11-libICE
BuildRequires:  xorg-x11-libSM
#Requires:       xorg-x11-libSM-devel
BuildRequires:  xorg-x11-libX11
#Requires:       xorg-x11-libX11-devel
%endif
#BuildRequires:  libXNVCtrl-devel
#BuildRequires:  texlive-latex
%if 0%{?suse_version} && 0%{?suse_version} <= 1220
BuildRequires:  texlive-bin-latex
#Requires:       texlive-bin-latex
%else
BuildRequires:  texlive-latex-bin
#Requires:       texlive-latex-bin
%endif
BuildRequires:  transfig
Requires:       transfig
BuildRequires:  w3m
#Requires:       w3m

BuildRequires:  zlib-%{compiler_family}%{PROJ_DELIM}
Requires:       zlib-%{compiler_family}%{PROJ_DELIM}

BuildRequires:  numactl-%{compiler_family}%{PROJ_DELIM}
Requires:       numactl-%{compiler_family}%{PROJ_DELIM}

%description
The Portable Hardware Locality (hwloc) software package provides
a portable abstraction (across OS, versions, architectures, ...)
of the hierarchical topology of modern architectures, including
NUMA memory nodes,  shared caches, processor sockets, processor cores
and processing units (logical processors or "threads"). It also gathers
various system attributes such as cache and memory information. It primarily
aims at helping applications with gathering information about modern
computing hardware so as to exploit it accordingly and efficiently.

hwloc may display the topology in multiple convenient formats.
It also offers a powerful programming interface (C API) to gather information
about the hardware, bind processes, and much more.

%prep
%setup -n %{pname}-%{version}

%build
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib
module load numactl

./configure --prefix=%{install_path} --enable-static

make %{?_smp_mflags} V=1

%install
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib
module load numactl

make %{?_smp_mflags} DESTDIR=%{buildroot} install

# documentation will be handled by % doc macro
%{__rm} -rf %{buildroot}%{install_path}/doc/ doc/doxygen-doc/man
%{__rm} -rf doc/.deps
%if 0%{?sles_version} || 0%{?suse_version}
%fdupes -s %{buildroot}/%{install_path}/share/man/man1
%fdupes -s %{buildroot}/%{install_path}/share/man/man3
%fdupes -s %{buildroot}/%{install_path}/share/man/man7
%fdupes -s doc/
%endif

# modulefile
%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} compiler toolchain."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: %{pname} library built with the %{compiler_family} compiler toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: library"
module-whatis "Description: %{summary}"

depends-on zlib
depends-on numactl

set             version             %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib
prepend-path    MANPATH             %{install_path}/share/man

prepend-path    CPATH               %{install_path}/include
prepend-path    FPATH               %{install_path}/include
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include
setenv          %{PNAME}_LIB        %{install_path}/lib

EOF

%{__mkdir_p} %{buildroot}/%{_docdir}

%files
%{OHPC_PUB}
%doc AUTHORS COPYING NEWS README VERSION
