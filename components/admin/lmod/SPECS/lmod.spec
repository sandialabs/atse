#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros

%define pname lmod

%if 0%{?suse_version} <= 1220
%define luaver 5.1
%else
%define luaver 5.2
%endif
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%define LUA_CPATH ?.so;?/?.so;%{lualibdir}/?.so
%define LUA_PATH ?.lua;?/?.lua;%{luapkgdir}/?.lua

Summary:   Lua based Modules (lmod)
Name:      %{pname}%{PROJ_DELIM}
Version:   7.8.1
Release:   1%{?dist}
License:   MIT
Group:     %{PROJ_NAME}/admin
Url:       https://github.com/TACC/Lmod
#Source0:   https://github.com/TACC/Lmod/archive/%{version}.tar.gz
Source0:   %{version}.tar.gz

BuildRequires: lua >= %{luaver}
BuildRequires: lua-devel >= %{luaver}
BuildRequires: lua-filesystem%{PROJ_DELIM}
BuildRequires: lua-posix%{PROJ_DELIM}

BuildRequires: rsync
BuildRequires: tcl

%if 0%{?sles_version} || 0%{?suse_version}
BuildRequires: procps
%endif

Provides: %{pname}

# TOSS3 packages "Require: Lmod"
Provides: Lmod

%if 0%{?sles_version} || 0%{?suse_version}
Conflicts: Modules
Provides:  Modules
%else
# HPE MPI and some other packages "Require: environment-modules". Lmod is compatible with environment-modules.
Conflicts: environment-modules
Provides:  environment-modules
Provides:  environment(modules)
%endif

# 8/28/14 karl.w.schulz@intel.com - include patches to remove consulting notice and setting of TACC env variables
Patch1: lmod.consulting.patch
Patch2: lmod.site.patch
# 4/25/17 karl.w.schulz@intel.com - upping patch fuzz factor for newer lmod
%global _default_patch_fuzz 2

# Known dependencies
Requires: lua >= %{luaver}
Requires: tcl
Requires: lua-filesystem%{PROJ_DELIM}
Requires: lua-posix%{PROJ_DELIM}

%description
Lmod: An Environment Module System based on Lua, Reads TCL Modules,
Supports a Software Hierarchy

%prep
%setup -q -n Lmod-%{version}

# OpenHPC patches
%patch1 -p1
%patch2 -p1

%build
unset MODULEPATH
export LUA_CPATH="%{LUA_CPATH}"
export LUA_PATH="%{LUA_PATH}"
./configure --prefix=%{OHPC_ADMIN} --libdir=%{lualibdir} --datadir=%{luapkgdir} --with-redirect=yes --with-autoSwap=no

%install
export LUA_CPATH="%{LUA_CPATH}"
export LUA_PATH="%{LUA_PATH}"
make DESTDIR=$RPM_BUILD_ROOT install
# Customize startup script to suit

%{__mkdir_p} %{buildroot}/%{_sysconfdir}/profile.d
%{__cat} << EOF > %{buildroot}/%{_sysconfdir}/profile.d/lmod.sh
#!/bin/sh
# -*- shell-script -*-
########################################################################
#  This is the system wide source file for setting up
#  modules:
#
########################################################################

# Root doesn't need to source lmod startup scripts
if [ $EUID -eq 0 ]; then
     return
fi

# NOOP if running under known resource manager
if [ ! -z "\$SLURM_NODELIST" ];then
     return
fi

if [ ! -z "\$PBS_NODEFILE" ];then
    return
fi

if [ ! -z "$LMOD_SETTARG_CMD" ];then
    . /opt/atse/lmod/lmod/init/bash >/dev/null
    return
fi

# Ensure MANPATH has a trailing : so system default manpath is included
if [ ! -z "\$MANPATH" ];then
    export MANPATH="\$MANPATH:"
fi

# Pick up man pages for lmod, make "man module" work
export MANPATH=/opt/atse/lmod/%{version}/share/man:\$MANPATH

export LMOD_SETTARG_CMD=":"
export LMOD_FULL_SETTARG_SUPPORT=no
export LMOD_COLORIZE=no
export LMOD_PREPEND_BLOCK=normal

if [ \$EUID -eq 0 ]; then
    export MODULEPATH=%{OHPC_MODULES}
else
    export MODULEPATH=%{OHPC_MODULES}
fi

export BASH_ENV=%{OHPC_ADMIN}/lmod/lmod/init/bash

# Initialize modules system
. %{OHPC_ADMIN}/lmod/lmod/init/bash >/dev/null

# Load baseline ATSE gnu7 programming environment
module try-add devpack-gnu7

EOF

%{__cat} << EOF > %{buildroot}/%{_sysconfdir}/profile.d/lmod.csh
#!/bin/csh
# -*- shell-script -*-
########################################################################
#  This is the system wide source file for setting up
#  modules:
#
########################################################################

#if ( \$?SLURM_NODELIST ) then
#    exit 0
#endif

#if ( \$?PBS_NODEFILE ) then
#    exit 0
#endif

if ( $?LMOD_SETTARG_CMD ) then
    source /opt/atse/lmod/lmod/init/csh >/dev/null
    exit 0
endif

# If MANPATH is undefined, define it.
# Ensure MANPATH has a trailing ":" so that the system default manpath is included.
if (! \$?MANPATH ) then
    setenv MANPATH ":"
else
    setenv MANPATH "\${MANPATH}:"
endif

# Pick up man pages for lmod, make "man module" work
setenv MANPATH /opt/atse/lmod/%{version}/share/man:\${MANPATH}

setenv LMOD_SETTARG_CMD ":"
setenv LMOD_FULL_SETTARG_SUPPORT "no"
setenv LMOD_COLORIZE "no"
setenv LMOD_PREPEND_BLOCK "normal"

if ( \`id -u\` == "0" ) then
   setenv MODULEPATH "%{OHPC_MODULES}"
else
   setenv MODULEPATH "%{OHPC_MODULES}"
endif

# Initialize modules system
source %{OHPC_ADMIN}/lmod/lmod/init/csh >/dev/null

# Load baseline ATSE gnu7 programming environment
module try-add devpack-gnu7

EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%dir %{OHPC_HOME}
%dir %{OHPC_ADMIN}
%{OHPC_ADMIN}/lmod
%config %{_sysconfdir}/profile.d/lmod.sh
%config %{_sysconfdir}/profile.d/lmod.csh
%{OHPC_PUB}
%doc License README.md README_lua_modulefiles.txt INSTALL
