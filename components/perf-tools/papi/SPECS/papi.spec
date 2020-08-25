#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname papi

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   Performance Application Programming Interface
Name:      %{pname}-%{compiler_family}%{PROJ_DELIM}
Version:   5.7.0
Release:   1%{?dist}
License:   BSD
Group:     %{PROJ_NAME}/perf-tools
URL:       http://icl.cs.utk.edu/papi/
#Source0:   http://icl.cs.utk.edu/projects/papi/downloads/papi-%{version}.tar.gz
Source0:   papi-%{version}.tar.gz
Patch1:    papi.ldconfig.patch
#Patch2:    armclang.patch

BuildRequires: ncurses-devel
%if 0%{?suse_version}
BuildRequires: gcc-fortran
%else
BuildRequires: gcc-gfortran
BuildRequires: chrpath
%endif
BuildRequires: kernel-headers >= 2.6.32
BuildRequires: libpfm-devel
Requires:      libpfm

%description
PAPI provides a programmer interface to monitor the performance of
running programs.

%prep
%setup -q -n %{pname}-%{version}
%patch1 -p1
#%patch2 -p1

%build
%ohpc_setup_autotools
%ohpc_setup_compiler

cd src
CFLAGS="-fPIC -DPIC" CXXFLAGS="-fPIC -DPIC" FCFLAGS="-fPIC" ./configure --with-static-lib=yes --with-shared-lib=yes --with-shlib-tools --prefix=%{install_path}
#DBG workaround to make sure libpfm just uses the normal CFLAGS
DBG="" CFLAGS="-fPIC -DPIC" CXXFLAGS="-fPIC -DPIC" FCFLAGS="-fPIC" make

%install
%ohpc_setup_autotools
%ohpc_setup_compiler

cd src
make DESTDIR=%{buildroot} install

# modulefile

%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

    puts stderr " "
    puts stderr "This module loads %{pname} built with the %{compiler_family} toolchain."
    puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: %{pname} built with the %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: performance tool"
module-whatis "Description: %{summary}"

set             version             %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib
prepend-path    MANPATH             %{install_path}/share/man

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include
setenv          %{PNAME}_LIB        %{install_path}/lib

EOF

%{__mkdir_p} %{buildroot}/%{_docdir}

%files
%{OHPC_PUB}
%doc ChangeLog*.txt INSTALL.txt LICENSE.txt README RELEASENOTES.txt
