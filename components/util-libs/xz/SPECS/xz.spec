#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname xz

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   Library and command line tools for XZ and LZMA compressed files
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   5.2.4
Release:   1%{?dist}
License:   LGPLv2+
Group:     %{PROJ_NAME}/libs
URL:       https://tukaani.org/xz
#Source0:   https://tukaani.org/xz/xz-5.2.4.tar.xz
Source0:   xz-5.2.4.tar.xz
Patch0:    rhel7.patch

%description
XZ Utils provide a general purpose data compression library
and command line tools. The native file format is the .xz
format, but also the legacy .lzma format is supported. The .xz
format supports multiple compression algorithms, of which LZMA2
is currently the primary algorithm. With typical files, XZ Utils
create about 30 percent smaller files than gzip.

%prep
%setup -n %{pname}-%{version}
%patch0 -p1

%build
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags

./configure --prefix=%{install_path}

make %{?_smp_mflags}

%install
%ohpc_setup_autotools
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
%doc ABOUT-NLS
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc COPYING.GPLv2
%doc COPYING.GPLv3
%doc COPYING.LGPLv2.1
%doc INSTALL
%doc INSTALL.generic
%doc NEWS
%doc PACKAGERS
%doc README
%doc THANKS
%doc TODO
