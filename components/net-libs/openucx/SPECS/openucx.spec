#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname openucx

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1
%define ohpc_mofed_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   UCX is a communication library implementing high-performance messaging
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   1.7.0
Release:   1%{?dist}
License:   BSD
Group:     %{PROJ_NAME}/libs
URL:       http://www.openucx.org
#Source0:   https://github.com/openucx/%{name}/releases/download/v%{version}/ucx-%{version}.tar.gz
Source0:   ucx-%{version}.tar.gz

# ATSE dependencies
BuildRequires: binutils%{PROJ_DELIM}
BuildRequires: numactl-%{compiler_family}%{PROJ_DELIM}
Requires:      numactl-%{compiler_family}%{PROJ_DELIM}
BuildRequires: zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:      zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}

%description
UCX stands for Unified Communication X. It requires either RDMA-capable device
(InfiniBand, RoCE, etc), Cray Gemini or Aries, for inter-node communication.
Future versions will support also TCP for inter-node, to lift that hardware
dependency.
In addition, the library can be used for intra-node communication by leveraging
the following shared memory mechanisms: posix. sysv, cma, knem, xpmem.

%prep
%setup -n ucx-%{version}

%build
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load numactl
module load zlib

# Only needed for github checkouts
#./autogen.sh

./configure \
        --prefix=%{install_path} \
        --enable-optimizations \
        --disable-logging \
        --disable-debug \
        --disable-assertions \
        --disable-params-check \
        --enable-mt \
        --with-pic

make %{?_smp_mflags} V=1

%install
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load numactl
module load zlib

make %{?_smp_mflags} DESTDIR=%{buildroot} V=1 install

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

depends-on numactl
depends-on zlib

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
%doc AUTHORS
%doc LICENSE
%doc NEWS
%doc README
