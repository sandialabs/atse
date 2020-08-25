%define pname ninja

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_UTILS}/%{pname}/%{version}

Summary:   A small build system with a focus on speed
Name:      %{pname}%{PROJ_DELIM}
Version:   1.8.2
Release:   1%{?dist}
License:   Apache License Version 2.0
Group:     %{PROJ_NAME}/dev-tools
URL:       https://ninja-build.org
#Source0:  https://github.com/ninja-build/ninja/archive/v%{version}.tar.gz

# Use Kitware patched version rather than official upstream
Source0:   https://github.com/Kitware/ninja/archive/v%{version}.g81279.kitware.dyndep-1.jobserver-1.tar.gz

BuildRequires: asciidoc
BuildRequires: gcc-c++

%description
A small build system with a focus on speed.

%prep
#%setup -n %{pname}-%{version}
%setup -n %{pname}-%{version}.g81279.kitware.dyndep-1.jobserver-1

%build
./configure.py --bootstrap
./ninja manual

%install
%{__mkdir_p} %{buildroot}/%{install_path}/bin
%{__mkdir_p} %{buildroot}/%{_docdir}
cp -p ninja %{buildroot}/%{install_path}/bin/

# modulefile

%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

	puts stderr "This module loads the %{pname} build tool"
	puts stderr "\nVersion %{version}\n"
	puts stderr " "

}

module-whatis "Name: %{pname}"
module-whatis "Version: %{version}"
module-whatis "Category: utility, developer support"
module-whatis "Keywords: System, Utility"
module-whatis "Description: Developer utilities"

prepend-path    PATH            %{install_path}/bin
EOF

%files
%{OHPC_PUB}
%doc COPYING
%doc README
%doc doc/manual.asciidoc
%doc doc/manual.html
