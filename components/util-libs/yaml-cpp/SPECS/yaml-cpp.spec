#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname yaml-cpp

%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   A YAML parser and emitter in C++
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   0.6.2
Release:   1%{?dist}
License:   MIT
Group:     %{PROJ_NAME}/util-libs
URL:       https://github.com/jbeder/yaml-cpp
#Source0:   https://github.com/jbeder/yaml-cpp/archive/yaml-cpp-%{version}.tar.gz
Source0:   yaml-cpp-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  cmake%{PROJ_DELIM}

%description
yaml-cpp is a YAML parser and emitter in C++ matching the YAML 1.2 spec.

%prep
%setup -n %{pname}-%{pname}-%{version}

%build
%ohpc_setup_compiler
%ohpc_setup_optflags
module load cmake

mkdir BUILD
cd BUILD

cmake	\
	-D CMAKE_INSTALL_PREFIX=%{install_path} \
	-D BUILD_SHARED_LIBS=ON \
	-D BUILD_STATIC_LIBS=ON \
	../

make %{?_smp_mflags} VERBOSE=1
cd ..

%install
%ohpc_setup_compiler
%ohpc_setup_optflags
module load cmake

cd BUILD
make %{?_smp_mflags} VERBOSE=1 DESTDIR=%{buildroot} install INSTALL='install -p'
cd ..

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

prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib

prepend-path    CPATH               %{install_path}/include
prepend-path    FPATH               %{install_path}/include
prepend-path    LIBRARY_PATH        %{install_path}/lib

setenv          YAML_CPP_DIR        %{install_path}
setenv          YAML_CPP_INC        %{install_path}/include
setenv          YAML_CPP_LIB        %{install_path}/lib

EOF

%{__mkdir_p} %{buildroot}/%{_docdir}

%files
%{OHPC_PUB}
%doc LICENSE
%doc README.md
