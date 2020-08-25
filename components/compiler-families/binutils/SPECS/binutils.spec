%define pname binutils

%define ohpc_autotools_dependent 1

%include %{_sourcedir}/OHPC_macros

Summary:   The GNU Binary Utilities
Name:      %{pname}%{PROJ_DELIM}
Version:   2.33.1
Release:   1%{?dist}
License:   GNU GPL and GNU LGPL
Group:     %{PROJ_NAME}/binary-tools
URL:       https://www.gnu.org/software/binutils/
#Source0:   https://ftp.gnu.org/gnu/binutils/%{pname}-%{version}.tar.gz
Source0:   %{pname}-%{version}.tar.gz

BuildRequires: flex
BuildRequires: bison
BuildRequires: gettext
BuildRequires: libstdc++-static

%define install_path %{OHPC_UTILS}/%{pname}/%{version}

%description
The GNU Binary Utilities.

%prep
%setup -n %{pname}-%{version}

%build
%ohpc_setup_autotools
./configure --prefix=%{install_path} --disable-dependency-tracking --disable-werror --enable-interwork --enable-multilib --enable-shared --enable-64-bit-bfd --enable-targets=all --with-sysroot=/ --enable-gold --enable-ld --enable-plugins --enable-lto --enable-install-libiberty
make %{_smp_mflags} MAKEINFO=true all

%install
%ohpc_setup_autotools
make DESTDIR=$RPM_BUILD_ROOT MAKEINFO=true install

# OpenHPC module file
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {
puts stderr "This module loads the GNU binary utilities."
puts stderr " "
}

module-whatis "Name: GNU binutils"
module-whatis "Version: %{version}"
module-whatis "Category: utility, developer tools"
module-whatis "Keywords: System, Utility, Toolchain"
module-whatis "Description: GNU binary utilities"

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib64
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib
prepend-path    MANPATH             %{install_path}/share/man

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_LIB64      %{install_path}/lib64

EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%{OHPC_PUB}
%doc ChangeLog
%doc COPYING
%doc COPYING.LIB
%doc COPYING3
%doc COPYING3.LIB
%doc MAINTAINERS
%doc README
