#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname git-lfs

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_UTILS}/%{pname}/%{version}

Summary:   Git large file support (lfs)
Name:      %{pname}%{PROJ_DELIM}
Version:   2.10.0
Release:   1%{?dist}
License:   MIT
Group:     %{PROJ_NAME}/dev-tools
URL:       https://git-lfs.github.com/
#Source0:   https://github.com/git-lfs/git-lfs/archive/v2.10.0.tar.gz
Source0:   git-lfs-%{version}.tar.gz
Source1:   git-lfs-%{version}-aarch64
Source2:   git-lfs-%{version}-x86_64

BuildRequires: go
BuildRequires: git%{PROJ_DELIM}
Requires:      git%{PROJ_DELIM}

%description
Git Large File Storage (LFS) replaces large files such as audio samples,
videos, datasets, and graphics with text pointers inside Git, while storing the
file contents on a remote server like GitHub.com or GitHub Enterprise.

%prep
%setup -n %{pname}-%{version}

%build
#make %{?_smp_mflags}
#make %{?_smp_mflags} man

%install

%ifarch aarch64
install -D %{SOURCE1} ${RPM_BUILD_ROOT}/%{install_path}/bin/git-lfs
%endif

%ifarch x86_64
install -D %{SOURCE2} ${RPM_BUILD_ROOT}/%{install_path}/bin/git-lfs
%endif

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {
        puts stderr " "
        puts stderr "This module loads the %{pname} add-on to git"
        puts stderr "\nVersion %{version}\n"
}
module-whatis "Name: %{pname}"
module-whatis "Version: %{version}"
module-whatis "Category: utility, developer support"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

prepend-path    PATH                %{install_path}/bin
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
