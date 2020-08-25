#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

%define pname bzip2

%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:   A lossless data-compression library
Name:      %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:   1.0.6
Release:   1%{?dist}
License:   BSD
Group:     %{PROJ_NAME}/libs
URL:       http://www.bzip.org/
Source0:   %{pname}-%{version}.tar.gz
Patch0:    bzip2-1.0.4-saneso.patch
Patch1:    bzip2-1.0.4-cflags.patch
Patch2:    bzip2-1.0.4-bzip2recover.patch
Patch3:    bzip2-1.0.6-makefile.patch

%description
The bzip2 lossless data-compression library.

%prep
%setup -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ohpc_setup_compiler
%ohpc_setup_optflags

# Build libbz2.so
make %{?_smp_mflags} -f Makefile-libbz2_so all
rm -f *.o

# Build libbz2.a and bz2 utilities
make %{?_smp_mflags} all

%install
%ohpc_setup_compiler
%ohpc_setup_optflags

%define PREFIX %{buildroot}/%{install_path}

# Install libbz2.a and bz2 utilities
# This is copied from the bzip2-1.0.6 Makefile
if ( test ! -d %{PREFIX}/bin ) ; then mkdir -p %{PREFIX}/bin ; fi
if ( test ! -d %{PREFIX}/lib ) ; then mkdir -p %{PREFIX}/lib ; fi
if ( test ! -d %{PREFIX}/man ) ; then mkdir -p %{PREFIX}/man ; fi
if ( test ! -d %{PREFIX}/man/man1 ) ; then mkdir -p %{PREFIX}/man/man1 ; fi
if ( test ! -d %{PREFIX}/include ) ; then mkdir -p %{PREFIX}/include ; fi
cp -f bzip2 %{PREFIX}/bin/bzip2
cp -f bzip2 %{PREFIX}/bin/bunzip2
cp -f bzip2 %{PREFIX}/bin/bzcat
cp -f bzip2recover %{PREFIX}/bin/bzip2recover
chmod a+x %{PREFIX}/bin/bzip2
chmod a+x %{PREFIX}/bin/bunzip2
chmod a+x %{PREFIX}/bin/bzcat
chmod a+x %{PREFIX}/bin/bzip2recover
cp -f bzip2.1 %{PREFIX}/man/man1
chmod a+r %{PREFIX}/man/man1/bzip2.1
cp -f bzlib.h %{PREFIX}/include
chmod a+r %{PREFIX}/include/bzlib.h
cp -f libbz2.a %{PREFIX}/lib
chmod a+r %{PREFIX}/lib/libbz2.a
cp -f bzgrep %{PREFIX}/bin/bzgrep
chmod a+x %{PREFIX}/bin/bzgrep
cp -f bzmore %{PREFIX}/bin/bzmore
chmod a+x %{PREFIX}/bin/bzmore
cp -f bzdiff %{PREFIX}/bin/bzdiff
chmod a+x %{PREFIX}/bin/bzdiff
cp -f bzgrep.1 bzmore.1 bzdiff.1 %{PREFIX}/man/man1
chmod a+r %{PREFIX}/man/man1/bzgrep.1
chmod a+r %{PREFIX}/man/man1/bzmore.1
chmod a+r %{PREFIX}/man/man1/bzdiff.1
echo ".so man1/bzgrep.1" > %{PREFIX}/man/man1/bzegrep.1
echo ".so man1/bzgrep.1" > %{PREFIX}/man/man1/bzfgrep.1
echo ".so man1/bzmore.1" > %{PREFIX}/man/man1/bzless.1
echo ".so man1/bzdiff.1" > %{PREFIX}/man/man1/bzcmp.1

# Install libbz2.so
cp -f libbz2.so.1.0.6 %{buildroot}/%{install_path}/lib

# Make symbolic links
cd %{PREFIX}/bin
ln -s -f bzgrep bzegrep
ln -s -f bzgrep bzfgrep
ln -s -f bzmore bzless
ln -s -f bzdiff bzcmp

cd %{PREFIX}/lib
chmod a+r libbz2.so.1.0.6
ln -s -f libbz2.so.1.0.6 libbz2.so.1.0
ln -s -f libbz2.so.1.0 libbz2.so.1
ln -s -f libbz2.so.1 libbz2.so

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
%doc CHANGES
%doc LICENSE
%doc README
%doc README.COMPILATION.PROBLEMS
%doc README.XML.STUFF
