%define with_slurm 1
%define with_tm    0
%define with_pmix  1
%define with_mofed 1
%define with_ucx   1

#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define pname openmpi3

%define ohpc_autotools_dependent 1
%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1
%define ohpc_mofed_dependent 1

%include %{_sourcedir}/OHPC_macros

# OpenMPI is possibly dependent on the RMS (workload manager)
%{!?RMS_DELIM: %global RMS_DELIM %{nil}}

%define with_openib 1

%ifarch aarch64 || ppc64le
%define with_psm 0
%define with_psm2 0
%else
%define with_psm 1
%define with_psm2 1
%endif

%{!?with_lustre: %define with_lustre 0}
%{!?with_slurm: %define with_slurm 0}
%{!?with_tm: %global with_tm 1}
%{!?with_pmix: %define with_pmix 0}
%{!?with_mofed: %define with_mofed 0}
%{!?with_ucx: %define with_ucx 0}
%{!?with_xpmem: %define with_xpmem 0}

Summary:   The OpenMPI implementation of MPI

Name:      %{pname}%{RMS_DELIM}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}

Version:   3.1.4
Release:   1%{?dist}
License:   BSD-3-Clause
Group:     %{PROJ_NAME}/mpi-families
URL:       http://www.open-mpi.org
#Source0:   http://www.open-mpi.org/software/ompi/v3.1/downloads/openmpi-%{version}.tar.bz2
Source0:   openmpi-%{version}.tar.bz2
Source3:   pbs-config
Patch0:    openmpi-3.0-pbs-config.patch

%if "%{RMS_DELIM}" != "%{nil}"
Provides: %{pname}-%{compiler_family}%{PROJ_DELIM}
Conflicts: %{pname}-%{compiler_family}%{PROJ_DELIM}
%endif

BuildRequires:  postfix
BuildRequires:  opensm
BuildRequires:  opensm-devel

BuildRequires:  zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Requires:       zlib-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}

BuildRequires:  numactl-%{compiler_family}%{PROJ_DELIM}
Requires:       numactl-%{compiler_family}%{PROJ_DELIM}

BuildRequires:  hwloc-%{compiler_family}%{PROJ_DELIM}
Requires:       hwloc-%{compiler_family}%{PROJ_DELIM}

%if %{with_ucx}
BuildRequires:  openucx-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
#Requires:       openucx-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
%endif

%if 0%{with_pmix}
BuildRequires:  pmix%{PROJ_DELIM}
Requires:       pmix%{PROJ_DELIM}
BuildRequires:  libevent-devel
Requires:       libevent-devel
%endif

%if 0%{?centos_version} == 700
BuildRequires: libtool-ltdl
Requires:      libtool-ltdl
%endif

%if 0%{with_slurm}
BuildRequires:  slurm-devel%{PROJ_DELIM}
Requires:       slurm-devel%{PROJ_DELIM}
BuildRequires:  slurm-libpmi%{PROJ_DELIM}
Requires:       slurm-libpmi%{PROJ_DELIM}
%endif

%if 0%{?suse_version}
BuildRequires:  sysfsutils
%else
BuildRequires:  libsysfs-devel
Requires:       libsysfs-devel
%endif

%if %{with_lustre}
BuildRequires:  lustre-client%{PROJ_DELIM}
%endif

#%if %{with_openib}
#BuildRequires:  rdma-core-devel
#%endif

%if %{with_psm}
BuildRequires:  infinipath-psm infinipath-psm-devel
%endif

%if %{with_tm}
BuildRequires:  pbspro-server%{PROJ_DELIM}
BuildRequires:  openssl-devel
%endif

%if "0%{?__requires_exclude}" == "0"
%global __requires_exclude ^libpbs.so.*$|libucm\\.so\\.0|libucp\\.so\\.0|libucs\\.so\\.0|libuct\\.so\\.0
%else
%global __requires_exclude %{__requires_exclude}|^libpbs.so.*$|libucm\\.so\\.0|libucp\\.so\\.0|libucs\\.so\\.0|libuct\\.so\\.0
%endif

%if %{with_psm2}
BuildRequires:  libpsm2-devel >= 10.2.0
%endif

#Requires: prun%{PROJ_DELIM} >= 1.2
#!BuildIgnore: post-build-checks

# Default library install path
%define install_path %{OHPC_MPI_STACKS}/%{pname}-%{compiler_family}/%version

%description

Open MPI is a project combining technologies and resources from several
other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in order to
build the best MPI library available.

This RPM contains all the tools necessary to compile, link, and run
Open MPI jobs.

%prep

%setup -q -n openmpi-%{version}
%patch0 -p1

%build
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib
module load numactl
module load hwloc

#BASEFLAGS="--prefix=%{install_path} --disable-static --enable-shared --disable-dlopen --enable-builtin-atomics --with-sge --enable-mpi-cxx"
BASEFLAGS="--prefix=%{install_path} --disable-static --enable-shared --enable-builtin-atomics --with-sge --enable-mpi-cxx"

# build against external pmix and libevent
%if 0%{with_pmix}
# Use SLURM's libpmi* rather than compatibility versions in pmix
%if 0%{with_slurm}
BASEFLAGS="$BASEFLAGS --with-pmi=/usr"
%endif
module load pmix
BASEFLAGS="$BASEFLAGS --with-pmix=${PMIX_DIR}"
BASEFLAGS="$BASEFLAGS --with-libevent=external --with-hwloc=external"
%endif

%if %{with_psm}
  BASEFLAGS="$BASEFLAGS --with-psm"
%endif
%if %{with_psm2}
  BASEFLAGS="$BASEFLAGS --with-psm2"
%endif
%if %{with_tm}
  BASEFLAGS="$BASEFLAGS --with-tm=/opt/pbs/"
%endif
%if %{with_openib}
  BASEFLAGS="$BASEFLAGS --with-verbs"
%endif
%if %{with_mofed}
  KNEM_DIR=$(find /opt -maxdepth 1 -type d -name "knem*" -print0)
  HCOLL_DIR=/opt/mellanox/hcoll
  BASEFLAGS="$BASEFLAGS --with-hcoll=$HCOLL_DIR --with-knem=$KNEM_DIR"
%endif
%if 0%{with_ucx}
module load openucx
BASEFLAGS="$BASEFLAGS --with-ucx=${OPENUCX_DIR}"
%endif
%if %{with_xpmem}
  module load xpmem
  BASEFLAGS="$BASEFLAGS --with-xpmem=${XPMEM_DIR}"
%endif
%if %{with_lustre}
  BASEFLAGS="$BASEFLAGS --with-io-romio-flags=--with-file-system=testfs+ufs+nfs+lustre"
%endif

export BASEFLAGS

%if %{with_tm}
cp %{SOURCE3} .
%{__chmod} 700 pbs-config
export PATH="./:$PATH"
%endif

./configure ${BASEFLAGS} || { cat config.log && exit 1; }

%if "%{compiler_family}" == "llvm" || "%{compiler_family}" == "arm"
%{__sed} -i -e 's#wl=""#wl="-Wl,"#g' libtool
%{__sed} -i -e 's#pic_flag=""#pic_flag=" -fPIC -DPIC"#g' libtool
%endif

make %{?_smp_mflags} V=1

%install
%ohpc_setup_autotools
%ohpc_setup_compiler
%ohpc_setup_optflags
module load zlib
module load numactl
module load hwloc

make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT V=1 install

# Remove .la files detected by rpm
rm $RPM_BUILD_ROOT/%{install_path}/lib/*.la

# rename prun to avoid namespace conflict with ohpc
%{__mv} $RPM_BUILD_ROOT/%{install_path}/bin/prun $RPM_BUILD_ROOT/%{install_path}/bin/prun.ompi
%{__mv} $RPM_BUILD_ROOT/%{install_path}/share/man/man1/prun.1 $RPM_BUILD_ROOT/%{install_path}/share/man/man1/prun.ompi.1

# OpenHPC module file
%{__mkdir_p} %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} compiler toolchain."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "URL: %{url}"

depends-on zlib
depends-on numactl
depends-on hwloc

set     version			    %{version}

setenv          MPI_DIR             %{install_path}
%if 0%{with_pmix}
setenv          OHPC_MPI_LAUNCHERS  pmix
%endif

prepend-path    PATH                %{install_path}/bin
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib
prepend-path    MANPATH             %{install_path}/share/man

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_INC        %{install_path}/include

prepend-path    MODULEPATH          %{OHPC_MODULEDEPS}/%{compiler_family}-%{pname}
prepend-path    MODULEPATH          %{OHPC_MODULEDEPS}/%{pname}
prepend-path    PKG_CONFIG_PATH     %{install_path}/lib/pkgconfig

setenv          MPICC               mpicc
setenv          MPICXX              mpicxx
setenv          MPIFC               mpifort
setenv          MPIF77              mpif77
setenv          MPIF90              mpif90

family "MPI"
EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%{install_path}
%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%doc NEWS
%doc README
%doc LICENSE
%doc AUTHORS
%doc README.JAVA.txt
