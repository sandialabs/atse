#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname git

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_UTILS}/%{pname}/%{version}

Summary:   Git distributed revision control system
Name:      %{pname}%{PROJ_DELIM}
Version:   2.26.2
Release:   1%{?dist}
License:   GPLv2
Group:     %{PROJ_NAME}/dev-tools
URL:       https://git-scm.com/
#Source0:   https://mirrors.edge.kernel.org/pub/software/scm/git/git-%{version}.tar.gz
Source0:   git-%{version}.tar.gz

BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: emacs
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: libcurl-devel
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: tk-devel
BuildRequires: perl-devel
BuildRequires: perl >= 0:5.008
# Following called out explicitly in git INSTALL
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::Temp)
BuildRequires: perl(Net::Domain)
BuildRequires: perl(Net::SMTP)
BuildRequires: perl(Time::HiRes)
# Following ar additional perl modules that seem to be needed
BuildRequires: perl(Mail::Address)
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Error)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::stat)
BuildRequires: perl(Term::ReadKey)
BuildRequires: perl(lib)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)

Requires:      zlib
Requires:      openssh-clients
Requires:      libcurl
Requires:      expat
Requires:      tk
Requires:      gettext
Requires:      less
Requires:      rsync
Requires:      perl >= 0:5.008
# Following called out explicitly in git INSTALL
Requires:      perl(Digest::MD5)
Requires:      perl(File::Spec)
Requires:      perl(File::Temp)
Requires:      perl(Net::Domain)
Requires:      perl(Net::SMTP)
Requires:      perl(Time::HiRes)
# Following ar additional perl modules that seem to be needed
Requires:      perl(Mail::Address)
Requires:      perl(Getopt::Long)
Requires:      perl(Error)
Requires:      perl(Exporter)
Requires:      perl(File::Basename)
Requires:      perl(File::Copy)
Requires:      perl(File::Find)
Requires:      perl(File::Path)
Requires:      perl(File::stat)
Requires:      perl(Term::ReadKey)
Requires:      perl(lib)
Requires:      perl(strict)
Requires:      perl(vars)
Requires:      perl(warnings)

%description
Git distributed revision control system

%prep
%setup -n %{pname}-%{version}

%build
./configure --prefix=%{install_path}

%install
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install install-doc

# Build the subtree extension (alternative to git submodule)
cd contrib/subtree
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install install-doc

# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {
        puts stderr " "
        puts stderr "This module loads the %{pname} library"
        puts stderr "\nVersion %{version}\n"
}
module-whatis "Name: %{pname}"
module-whatis "Version: %{version}"
module-whatis "Category: utility, developer support"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

prepend-path    PATH                %{install_path}/bin
prepend-path    MANPATH             %{install_path}/share/man
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
%doc COPYING
%doc README.md
