#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname powerapi

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   A reference implementation for the Power API specification
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   20200529
Release:   1%{?dist}
License:   MIT
Group:     %{PROJ_NAME}/util-libs
URL:       https://github.com/pwrapi/pwrapi-ref
Source0:   powerapi-%{version}.tar.gz

BuildRequires:  python
Requires:       python

BuildRequires:  python-devel
Requires:       python-devel

BuildRequires:  swig
Requires:       swig

BuildRequires:  numactl-%{compiler_family}%{PROJ_DELIM}
Requires:       numactl-%{compiler_family}%{PROJ_DELIM}

BuildRequires:  hwloc-%{compiler_family}%{PROJ_DELIM}
Requires:       hwloc-%{compiler_family}%{PROJ_DELIM}

BuildRequires:  tx2mon%{PROJ_DELIM}
Requires:       tx2mon%{PROJ_DELIM}

%description
A reference implementation for the Power API specification.

%prep
%setup -n %{pname}-%{version}

%build
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load numactl
module load hwloc

./autogen.sh
./configure --prefix=%{install_path} --with-hwloc=$HWLOC_DIR --with-tx2mon=/usr/include/tx2mon

make %{?_smp_mflags} V=1

%install
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load numactl
module load hwloc

make %{?_smp_mflags} V=1 DESTDIR=%{buildroot} install

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
depends-on hwloc

set             version             %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib

prepend-path    CPATH               %{install_path}/include
prepend-path    FPATH               %{install_path}/include
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include
setenv          %{PNAME}_LIB        %{install_path}/lib

# BEGIN: PowerAPI specific configuration
prepend-path    DYLD_LIBRARY_PATH   %{install_path}/lib
setenv          POWERAPI_DEBUG      0
setenv          POWERAPI_ROOT       "plat"
setenv          POWERAPI_CONFIG     %{install_path}/config/astra.hwloc
# END: PowerAPI specific configuration

EOF

%{__mkdir_p} %{buildroot}/%{_docdir}

%files
%{OHPC_PUB}
%doc LICENSE
%doc README
%doc VERSION
