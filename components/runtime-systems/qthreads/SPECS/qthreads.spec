#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname qthreads

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

%include %{_sourcedir}/OHPC_macros

%define install_path %{OHPC_LIBS}/%{compiler_family}/%{pname}/%{version}

Summary:       Qthreads runtime system for spawning and controlling coroutines
Name:          %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:       1.14
Release:       1%{?dist}
License:       BSD-3-Clause
Group:         %{PROJ_NAME}/runtimes
URL:           http://www.cs.sandia.gov/qthreads/
#Source0:      https://github.com/Qthreads/qthreads/releases/download/%{version}/%{pname}-%{version}.tar.bz2
Source0:       %{pname}-%{version}.tar.bz2

BuildRequires: hwloc-%{compiler_family}%{PROJ_DELIM}
Requires:      hwloc-%{compiler_family}%{PROJ_DELIM}

%description
The qthreads API is designed to make using large numbers of threads convenient
and easy. The API maps well to both MTA-style threading and PIM-style
threading, and is still quite useful in a standard SMP context. The qthreads
API also provides access to full/empty-bit (FEB) semantics, where every word of
memory can be marked either full or empty, and a thread can wait for any word
to attain either state.

The qthreads library on an SMP is essentially a library for spawning and
controlling coroutines: threads with small (4-8k) stacks. The threads are
entirely in user-space and use their locked/unlocked status as part of their
scheduling.

The library's metaphor is that there are many qthreads and several "shepherds".
Shepherds generally map to specific processors or memory regions, but this is
not an explicit part of the API. Qthreads are assigned to specific shepherds
and do not generally migrate.

The API includes utility functions for making threaded loops, sorting, and
similar operations convenient.

%prep
%setup -n %{pname}-%{version}

%build
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load hwloc

./configure --prefix=%{install_path} --with-topology=hwloc --with-hwloc=${HWLOC_DIR} \
            --enable-static --with-scheduler=distrib            \
            --disable-spawn-cache --with-default-stack-size=8192

make %{?_smp_mflags} V=1

#make check

%install
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load hwloc

make %{?_smp_mflags} DESTDIR=%{buildroot} V=1 install

# modulefile

%{__mkdir_p} %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library for the %{compiler_family} compiler toolchain."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: %{pname} runtime built with the %{compiler_family} compiler toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: runtime system"
module-whatis "Description: %{summary}"

depends-on    hwloc

set           version             %{version}

prepend-path  PATH                %{install_path}/bin
prepend-path  INCLUDE             %{install_path}/include
prepend-path  LD_LIBRARY_PATH     %{install_path}/lib
prepend-path  MANPATH             %{install_path}/share/man

prepend-path  CPATH               %{install_path}/include
prepend-path  FPATH               %{install_path}/include
prepend-path  LIBRARY_PATH        %{install_path}/lib

setenv        %{PNAME}_DIR        %{install_path}
setenv        %{PNAME}_BIN        %{install_path}/bin
setenv        %{PNAME}_INC        %{install_path}/include
setenv        %{PNAME}_LIB        %{install_path}/lib

EOF

%{__mkdir_p} %{buildroot}/%{_docdir}

%files
%{OHPC_PUB}
%doc AUTHORS
%doc COPYING
%doc NEWS
%doc README.affinity
%doc README.md
%doc README.multinode
%doc README.performance-monitoring.md
%doc SCHEDULING
%doc TODO.md
