#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname zlib

%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   A lossless data-compression library
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   1.2.11
Release:   1%{?dist}
License:   zlib and Boost
Group:     %{PROJ_NAME}/libs
URL:       http://www.zlib.net/
#Source0:   https://www.zlib.net/zlib-%{version}.tar.xz
Source0:   zlib-%{version}.tar.xz

%description
zlib is designed to be a free, general-purpose, legally unencumbered -- that
is, not covered by any patents -- lossless data-compression library for use on
virtually any computer hardware and operating system.

%prep
%setup -n %{pname}-%{version}

%build
%ohpc_setup_compiler
%ohpc_setup_optflags

# zlib doesn't actually use autotools
./configure --prefix=%{install_path}

%install
%ohpc_setup_compiler
%ohpc_setup_optflags

make %{?_smp_mflags} DESTDIR=%{buildroot} install

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
%doc README
%doc ChangeLog
%doc FAQ
