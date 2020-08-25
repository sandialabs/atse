#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%global pname arm-compilers-devel

%include %{_sourcedir}/OHPC_macros

Summary:     Arm Compiler for HPC compatibility package
Name:        %{pname}%{PROJ_DELIM}
Version:     20.1
Release:     1%{?dist}
License:     Apache-2.0
URL:         https://github.com/openhpc/ohpc
Group:       %{PROJ_NAME}/compiler-families
ExcludeArch: x86_64

# Depends on Arm-HPC Compiler for HPC
BuildRequires: arm-compiler-for-linux-20.1_Generic-AArch64_RHEL-7_aarch64-linux
BuildRequires: arm-linux-compiler-20.1_Generic-AArch64_RHEL-7_aarch64-linux
BuildRequires: armpl-20.1.0_Generic-AArch64_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
BuildRequires: armpl-20.1.0_Generic-SVE_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
BuildRequires: armpl-20.1.0_Neoverse-N1_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
BuildRequires: armpl-20.1.0_ThunderX2CN99_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
BuildRequires: armpl-20.1.0_A64FX_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
Requires: arm-compiler-for-linux-20.1_Generic-AArch64_RHEL-7_aarch64-linux
Requires: arm-linux-compiler-20.1_Generic-AArch64_RHEL-7_aarch64-linux
Requires: armpl-20.1.0_Generic-AArch64_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
Requires: armpl-20.1.0_Generic-SVE_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
Requires: armpl-20.1.0_Neoverse-N1_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
Requires: armpl-20.1.0_ThunderX2CN99_RHEL-7_arm-linux-compiler_20.1_aarch64-linux
Requires: armpl-20.1.0_A64FX_RHEL-7_arm-linux-compiler_20.1_aarch64-linux

# These provides are a HACK
# TODO: Ask Arm to fix their RPMs to include correct provides.
Provides: libflang.so()(64bit)
Provides: libflangrti.so()(64bit)
Provides: libompstub.so()(64bit)
Provides: libomp.so()(64bit)
Provides: libomp.so(VERSION)(64bit)
Provides: libarmflang.so()(64bit)
Provides: libstdc++.so.6(GLIBCXX_3.4.21)(64bit)
Provides: libstdc++.so.6(GLIBCXX_3.4.26)(64bit)
Provides: libamath_generic.so()(64bit)
Provides: libastring_generic.so()(64bit)
Provides: libamath_thunderx2t99.so()(64bit)
Provides: libastring_thunderx2t99.so()(64bit)
Provides: libomp_with_lse.so()(64bit)
Provides: libomp_with_lse.so(VERSION)(64bit)

%description
Arm Compiler for HPC provides C (armclang), C++ (armclang++), and
Fortran (armflang) compilers and supporting tools.

%define gcc_install_path /opt/arm/gcc-9.2.0_Generic-AArch64_RHEL-7_aarch64-linux
%define arm_install_path /opt/arm/arm-linux-compiler-20.1_Generic-AArch64_RHEL-7_aarch64-linux

%install

# modulefile

%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/arm
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/arm/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Arm Compiler for HPC, providing armclang, armclang++, and armflang."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name:  Arm Compiler for HPC"
module-whatis "Version: %{version}"
module-whatis "Category: compiler, runtime support"
module-whatis "Description: This module loads the Arm Compiler for HPC, providing armclang, armclang++, and armflang."

depends-on      binutils

# BEGIN: The Arm compilers depend on a base gcc installation
prepend-path    PATH                    %{gcc_install_path}/bin
prepend-path    LD_LIBRARY_PATH         %{gcc_install_path}/lib
prepend-path    LD_LIBRARY_PATH         %{gcc_install_path}/lib64
prepend-path    LIBRARY_PATH            %{gcc_install_path}/lib
prepend-path    LIBRARY_PATH            %{gcc_install_path}/lib64
prepend-path    CPATH                   %{gcc_install_path}/include
prepend-path    MANPATH                 %{gcc_install_path}/share/man
append-path     GCC_LIBRARIES           %{gcc_install_path}/lib
append-path     GCC_LIBRARIES           %{gcc_install_path}/lib64
setenv          GCC_DIR                 %{gcc_install_path}
setenv          GCC_INCLUDES            %{gcc_install_path}/include
setenv          COMPILER_PATH           %{gcc_install_path}
setenv          GCC_BUILD               5
# END: The Arm compilers depend on a base gcc installation

# BEGIN: Standard OpenHPC environment variables
set             version                 %{version}
prepend-path    PATH                    %{arm_install_path}/bin
prepend-path    INCLUDE                 %{arm_install_path}/include
prepend-path    LD_LIBRARY_PATH         %{arm_install_path}/lib
prepend-path    MANPATH                 %{arm_install_path}/share/man
prepend-path    MODULEPATH              %{OHPC_MODULEDEPS}/arm
# END: Standard OpenHPC environment variables

# BEGIN: Additional environment variables set by Arm's "official" module
setenv          ARM_LINUX_COMPILER_BUILD              15
setenv          ARM_LINUX_COMPILER_DIR                %{arm_install_path}
setenv          ARM_LINUX_COMPILER_INCLUDES           %{arm_install_path}/include
prepend-path    CPATH                                 %{arm_install_path}/include
prepend-path    LIBRARY_PATH                          %{arm_install_path}/lib
append-path     ARM_LINUX_COMPILER_LIBRARIES          %{arm_install_path}/lib
append-path     ARM_HPC_COMPILER_LICENSE_SEARCH_PATH  /opt/arm/licences:/opt/arm/licenses
append-path     LD_LIBRARY_PATH                       %{arm_install_path}/lib/clang/9.0.1/armpl_links/lib
# END: Additional environment variables set by Arm's "official" module

setenv CC  armclang
setenv CXX armclang++
setenv FC  armflang
setenv F77 armflang
setenv F90 armflang

family "compiler"
EOF

%files
%{OHPC_PUB}
