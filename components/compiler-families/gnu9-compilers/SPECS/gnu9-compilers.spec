# Set default config.
# This is needed because OBS source download service doesn't parse OHPC_macros.
%{!?compiler_family:  %define compiler_family  gnu9}
%{!?compiler_version: %define compiler_version 9.3.0}

#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define ohpc_autotools_dependent 1

%include %{_sourcedir}/OHPC_macros

%if "%{compiler_family}" == "gnu9"
%global gnu_version %{compiler_version}
%global gnu_major_ver 9
%global gnu_release 3
%global pname gnu9-compilers
%global source https://ftp.gnu.org/gnu/gcc/gcc-%{gnu_version}/gcc-%{gnu_version}.tar.xz
%global source_directory gcc-%{version}
%endif

%if "%{compiler_family}" == "gnu8"
%global gnu_version %{compiler_version}
%global gnu_major_ver 8
%global gnu_release 1
%global pname gnu8-compilers
%global source https://ftp.gnu.org/gnu/gcc/gcc-%{gnu_version}/gcc-%{gnu_version}.tar.xz
%global source_directory gcc-%{version}
%endif

%if "%{compiler_family}" == "gnu7"
%global gnu_version %{compiler_version}
%global gnu_major_ver 7
%global gnu_release 1
%global pname gnu7-compilers
%global source https://ftp.gnu.org/gnu/gcc/gcc-%{gnu_version}/gcc-%{gnu_version}.tar.xz
%global source_directory gcc-%{version}
%endif

# Define subcomponent versions required for build

%global gmp_version 6.1.0
%global mpfr_version 3.1.4
%global mpc_version 1.0.3
%global isl_version 0.18

Summary:   The GNU C Compiler and Support Files
Name:      %{pname}%{PROJ_DELIM}
Version:   %{gnu_version}
Release:   %{gnu_release}%{?dist}
License:   GNU GPL
Group:     %{PROJ_NAME}/compiler-families
URL:       http://gcc.gnu.org/
#Source0:   %{source}
#Source1:   ftp://gcc.gnu.org/pub/gcc/infrastructure/gmp-%{gmp_version}.tar.bz2
#Source2:   ftp://gcc.gnu.org/pub/gcc/infrastructure/mpfr-%{mpfr_version}.tar.bz2
#Source3:   ftp://gcc.gnu.org/pub/gcc/infrastructure/mpc-%{mpc_version}.tar.gz
#Source4:   ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Source0:   %{source}
Source1:   gmp-%{gmp_version}.tar.bz2
Source2:   mpfr-%{mpfr_version}.tar.bz2
Source3:   mpc-%{mpc_version}.tar.gz
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
%if 0%{?sles_version} || 0%{?suse_version}
BuildRequires:  fdupes
%endif
BuildRequires:  glibc-devel
BuildRequires:  glibc-static
BuildRequires:  libstdc++-devel
BuildRequires:  libstdc++-static
Requires:       glibc-devel
Requires:       glibc-static
Requires:       libstdc++-devel
Requires:       libstdc++-static
Requires:       binutils%{PROJ_DELIM}

%define install_path %{OHPC_COMPILERS}/gcc/%{version}

%description

Core package for the GNU Compiler Collection, including the C language
frontend.

%prep
%setup -q -n %{source_directory} -a1 -a2 -a3 -a4

ln -s gmp-%{gmp_version} gmp
ln -s mpfr-%{mpfr_version} mpfr
ln -s mpc-%{mpc_version} mpc
ln -s isl-%{isl_version} isl

%build
%ohpc_setup_autotools
module load binutils
%{__mkdir} obj
cd obj
../configure --prefix=%{install_path} --disable-multilib --enable-languages="c,c++,fortran" --enable-lto --with-quad --enable-gold --enable-ld --enable-frame-pointer
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
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/gnu%{gnu_major_ver}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/gnu%{gnu_major_ver}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the GNU compiler collection"
puts stderr " "
puts stderr "See the man pages for gcc, g++, and gfortran for detailed information"
puts stderr "on available compiler options and command-line syntax."
puts stderr " "

puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: GNU Compiler Collection"
module-whatis "Version: %{version}"
module-whatis "Category: compiler, runtime support"
module-whatis "Description: GNU Compiler Family (C/C++/Fortran for x86_64)"
module-whatis "URL: http://gcc.gnu.org/"

depends-on    binutils

set           version             %{version}

prepend-path  PATH                %{install_path}/bin
prepend-path  MANPATH             %{install_path}/share/man
prepend-path  INCLUDE             %{install_path}/include
prepend-path  LD_LIBRARY_PATH     %{install_path}/lib64
prepend-path  MODULEPATH          %{OHPC_MODULEDEPS}/%{compiler_family}

setenv CC  gcc
setenv CXX g++
setenv FC  gfortran
setenv F77 gfortran
setenv F90 gfortran

family "compiler"
EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/gnu%{gnu_major_ver}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%{OHPC_MODULES}/gnu%{gnu_major_ver}/
%dir %{OHPC_COMPILERS}/gcc
%{install_path}
%doc COPYING
%doc COPYING3
%doc COPYING3.LIB
%doc README
%doc ChangeLog.tree-ssa
%doc ChangeLog
%doc COPYING.LIB
%doc COPYING.RUNTIME
%if "%{compiler_family}" != "gnu7"
%doc NEWS
%endif
