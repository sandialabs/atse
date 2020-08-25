%global pname armpl

%define ohpc_compiler_dependent 1
%define ohpc_uarch_dependent 1

# Version numbers of the arm and gnu compilers
%define arm_version 20.1
%define gnu_version 9.2.0

# Build of the ARMPL libraries, must extract from each new version
%define armpl_build 7

%include %{_sourcedir}/OHPC_macros

Summary:     Arm Performance Libraries
Name:        %{pname}-%{compiler_family}%{UARCH_DELIM}%{PROJ_DELIM}
Version:     20.1.0
Release:     1%{?dist}
License:     Apache-2.0
URL:         https://github.com/openhpc/ohpc
Group:       %{PROJ_NAME}/math-libs
ExcludeArch: x86_64

%description
The Arm Performance Libraries provide optimized implementations of BLAS,
LAPACK, FFT and other math routines.

# ARMPL for Generic ARMv8 Architecture
%if "%{uarch}" == "generic"
%if "%{compiler_family}" == "arm"
%define install_path /opt/arm/armpl-%{version}_Generic-AArch64_RHEL-7_arm-linux-compiler_%{arm_version}_aarch64-linux
%endif
%if "%{compiler_family}" == "gnu7"
%define install_path /opt/arm/armpl-%{version}_Generic-AArch64_RHEL-7_gcc_%{gnu_version}_aarch64-linux
%endif
%if "%{compiler_family}" == "gnu8"
%define install_path /opt/arm/armpl-%{version}_Generic-AArch64_RHEL-7_gcc_%{gnu_version}_aarch64-linux
%endif
%if "%{compiler_family}" == "gnu9"
%define install_path /opt/arm/armpl-%{version}_Generic-AArch64_RHEL-7_gcc_%{gnu_version}_aarch64-linux
%endif
%endif

# ARMPL for Cavium ThunderX2 CN99XX Architecture
%if "%{uarch}" == "tx2"
%if "%{compiler_family}" == "arm"
%define install_path /opt/arm/armpl-%{version}_ThunderX2CN99_RHEL-7_arm-linux-compiler_%{arm_version}_aarch64-linux
%endif
%if "%{compiler_family}" == "gnu7"
%define install_path /opt/arm/armpl-%{version}_ThunderX2CN99_RHEL-7_gcc_%{gnu_version}_aarch64-linux
%endif
%if "%{compiler_family}" == "gnu8"
%define install_path /opt/arm/armpl-%{version}_ThunderX2CN99_RHEL-7_gcc_%{gnu_version}_aarch64-linux
%endif
%if "%{compiler_family}" == "gnu9"
%define install_path /opt/arm/armpl-%{version}_ThunderX2CN99_RHEL-7_gcc_%{gnu_version}_aarch64-linux
%endif
%endif

%install

# modulefile

%{__mkdir_p} %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Arm Performance Libraries for the %{compiler_family} toolchain."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: %{pname} for the %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: math libraries"
module-whatis "Description: %{summary}"

set             version                 %{version}

# Standard OpenHPC environment variables
prepend-path    PATH                    %{install_path}/bin
prepend-path    INCLUDE                 %{install_path}/include
prepend-path    LD_LIBRARY_PATH         %{install_path}/lib
prepend-path    MANPATH                 %{install_path}/share/man

setenv          %{PNAME}_DIR            %{install_path}
setenv          %{PNAME}_BIN            %{install_path}/bin
setenv          %{PNAME}_INC            %{install_path}/include
setenv          %{PNAME}_LIB            %{install_path}/lib

# Other misc. environment variables set by Arm's "official" module
setenv          ARMPL_DIR               %{install_path}
setenv          ARMPL_BUILD             %{armpl_build} 
setenv          ARMPL_INCLUDES          %{install_path}/include

prepend-path    CPATH                   %{install_path}/include_common
prepend-path    LIBRARY_PATH            %{install_path}/lib
append-path     ARMPL_LIBRARIES         %{install_path}/lib

setenv          LAPACK                  %{install_path}/lib/libarmpl_lp64.a
setenv          LAPACK_STATIC           %{install_path}/lib/libarmpl_lp64.a
setenv          LAPACK_SHARED           %{install_path}/lib/libarmpl_lp64.so
setenv          BLAS                    %{install_path}/lib/libarmpl_lp64.a
setenv          BLAS_STATIC             %{install_path}/lib/libarmpl_lp64.a
setenv          BLAS_SHARED             %{install_path}/lib/libarmpl_lp64.so
setenv          ARMPL_INCLUDES_MP       %{install_path}/include_lp64_mp
setenv          ARMPL_INCLUDES_LP64_MP  %{install_path}/include_lp64_mp
setenv          ARMPL_INCLUDES_INT64    %{install_path}/include_ilp64
setenv          ARMPL_INCLUDES_INT64_MP %{install_path}/include_ilp64_mp
setenv          ARMPL_INCLUDES_ILP64    %{install_path}/include_ilp64
setenv          ARMPL_INCLUDES_ILP64_MP %{install_path}/include_ilp64_mp

EOF

%files
%{OHPC_PUB}
