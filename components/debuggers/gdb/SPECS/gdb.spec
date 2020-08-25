#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname gdb

%define ohpc_autotools_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_TOOLS}/%{pname}/%{version}

# Define subcomponent versions required for build
%global gmp_version 6.1.2
%global mpc_version 1.1.0
%global mpfr_version 4.0.1
%global isl_version 0.18

Summary:   The GNU GDB Debugger
Name:      %{pname}%{PROJ_DELIM}
Version:   8.2
Release:   1%{?dist}
License:   GNU GPL
Group:     %{PROJ_NAME}/debuggers
URL:       http://gcc.gnu.org/
#Source0:  https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz
#Source1:  https://ftp.gnu.org/gnu/gmp/gmp-%{gmp_version}.tar.bz2
#Source2:  https://ftp.gnu.org/gnu/mpc/mpc-%{mpc_version}.tar.gz
#Source3:  https://ftp.gnu.org/gnu/mpfr/mpfr-%{mpfr_version}.tar.gz
#Source4:  ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Source0:   gdb-%{version}.tar.xz
Source1:   gmp-%{gmp_version}.tar.bz2
Source2:   mpc-%{mpc_version}.tar.gz
Source3:   mpfr-%{mpfr_version}.tar.gz
Source4:   isl-%{isl_version}.tar.bz2

BuildRequires:  binutils%{PROJ_DELIM}
BuildRequires:  m4
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gettext-devel
BuildRequires:  perl
BuildRequires:  gcc-c++
%if 0%{?suse_version} > 1220
BuildRequires:  makeinfo
%else
BuildRequires:  texinfo
%endif
BuildRequires:  zlib-devel
BuildRequires:  xz-devel
%if 0%{?sles_version} || 0%{?suse_version}
BuildRequires:  fdupes
%endif
BuildRequires:  glibc-devel
BuildRequires:  glibc-static
BuildRequires:  libstdc++-devel
BuildRequires:  libstdc++-static
BuildRequires:  expat-devel
BuildRequires:  python-devel
Requires:       glibc-devel
Requires:       glibc-static
Requires:       libstdc++-devel
Requires:       libstdc++-static
Requires:       binutils%{PROJ_DELIM}
Requires:       expat
Requires:       python

%description
The GNU GDB Debugger.

%prep
%setup -q -n %{pname}-%{version} -a1 -a2 -a3 -a4

ln -s gmp-%{gmp_version} gmp
ln -s mpc-%{mpc_version} mpc
ln -s mpfr-%{mpfr_version} mpfr
ln -s isl-%{isl_version} isl

%build
%ohpc_setup_autotools
module load binutils

%{__mkdir} obj
cd obj
../configure --prefix=%{install_path} --enable-lto --with-quad --enable-gold --enable-ld
make %{?_smp_mflags}

%install
%ohpc_setup_autotools
module load binutils

cd obj
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install

%if 0%{?sles_version} || 0%{?suse_version}
%fdupes -s $RPM_BUILD_ROOT/%{install_path}/include
%fdupes -s $RPM_BUILD_ROOT/%{install_path}/lib
%fdupes -s $RPM_BUILD_ROOT/%{install_path}/install-tools
%fdupes -s $RPM_BUILD_ROOT/%{install_path}/share
%endif

# OpenHPC module file
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the GNU gdb debugger"
puts stderr " "
puts stderr "See the man pages for gdb for detailed information"
puts stderr "on available compiler options and command-line syntax."
puts stderr " "

puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: GNU GDB Debugger"
module-whatis "Version: %{version}"
module-whatis "Category: debugger"
module-whatis "Description: GNU GDB Debugger"
module-whatis "URL: http://gcc.gnu.org/"

depends-on    binutils

set           version             %{version}

prepend-path  PATH                %{install_path}/bin
prepend-path  MANPATH             %{install_path}/share/man

family "debugger"
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
%doc ChangeLog
%doc COPYING
%doc COPYING.LIB
%doc COPYING3
%doc COPYING3.LIB
%doc MAINTAINERS
%doc gdb/README
