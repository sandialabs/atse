#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname spack

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_PUB}/%{pname}/%version

Name:		%{pname}%{PROJ_DELIM}
Version:	0.14.2
Release:	1%{?dist}
Summary:	HPC software package management

Group:		%{PROJ_NAME}/dev-tools
License:	Apache-2.0 or MIT at user's option
URL:		https://github.com/spack/spack
#Source0:	https://github.com/%{pname}/%{pname}/archive/%{pname}-%{version}.tar.gz
Source0:	%{pname}-%{version}.tar.gz
Patch0:		atse.patch

BuildArch: noarch
BuildRequires:	rsync
BuildRequires:	python
Requires:	python >= 2.6
Requires: bash
Requires: curl
Requires: coreutils
Requires: subversion
Requires: hg
Requires: patch

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%description
Spack is a package management tool designed to support multiple versions and
configurations of software on a wide variety of platforms and environments. It
was designed for large supercomputing centers, where many users and application
teams share common installations of software on clusters with exotic
architectures, using libraries that do not have a standard ABI. Spack is
non-destructive: installing a new version does not break existing
installations, so many configurations can coexist on the same system.

Most importantly, Spack is simple. It offers a simple spec syntax so that users
can specify versions and configuration options concisely. Spack is also simple
for package authors: package files are written in pure Python, and specs allow
package authors to write a single build script for many different builds of the
same package.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%install
mkdir -p %{buildroot}%{install_path}
rsync -av --exclude=.gitignore {etc,bin,lib,var,share} %{buildroot}%{install_path}

# Make config file needed for atse extensions to spack
%{__mkdir} -p %{buildroot}%{install_path}/opt/spack/.spack-db/
%{__cat} << EOF > %{buildroot}%{install_path}/opt/spack/.spack-db/index.json
{
  "database": {
    "installs": {},
    "version": "5"
  }
}
EOF

# OpenHPC module file
%{__mkdir} -p %{buildroot}/%{OHPC_PUB}/modulefiles/spack
%{__cat} << EOF > %{buildroot}/%{OHPC_PUB}/modulefiles/spack/%{version}
#%Module1.0#####################################################################

module-whatis "Name: Spack"
module-whatis "Version: %{version}"
module-whatis "Category: System/Configuration"
module-whatis "Description: Spack package management"
module-whatis "URL: https://github.com/spack/spack"

# Standard OpenHPC config
set             version             %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    MODULEPATH          %{install_path}/modules

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_LIB        %{install_path}/lib

# Spack specific config
setenv          SPACK_ROOT          %{install_path}

EOF

%{__mkdir} -p %{buildroot}/%{_docdir}

%files
%{OHPC_HOME}
%doc COPYRIGHT
%doc LICENSE-APACHE
%doc LICENSE-MIT
%doc NOTICE
%doc README.md
