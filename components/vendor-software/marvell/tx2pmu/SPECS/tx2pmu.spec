#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

# Define the kernel version to build thunderx2_pmu-v1.ko against.
# This is the output of `uname -r` on the target system.
%define kernel_version 4.14.0-115.el7a.aarch64

%define pname tx2pmu

%include %{_sourcedir}/OHPC_macros

Summary:     Extra uncore performance counters for Marvell ThunderX2 System on a Chip
Name:        %{pname}%{PROJ_DELIM}
Version:     20191029
Release:     1%{?dist}
License:     GPLv2
Group:       %{PROJ_NAME}/tools
URL:         https://github.com
#Source0:    https://github.com/gpkulkarni/module_tx2_pmu
Source0:     %{pname}-%{version}.tar.gz
ExcludeArch: x86_64

BuildRequires: gcc
BuildRequires: kernel
BuildRequires: kernel-devel
BuildRequires: ncurses-devel
Requires: kernel
Requires: ncurses

%description
Extra uncore performance counters for the Marvell ThunderX2 System on a Chip.

%prep
%setup -n %{pname}-%{version}

%build

# Build for the desired kernel version
sed -i 's/\$(shell uname -r)/%{kernel_version}/g' Makefile

# For Linux kernel versions 4.16 and below, need to do "make VERSION=-v1"
# For newer kernels just "make"
make VERSION=-v1

%install
# Install the thunderx2_pmu kernel module
%{__mkdir_p} %{buildroot}/lib/modules/%{kernel_version}/extra
cp thunderx2_pmu-v1.ko %{buildroot}/lib/modules/%{kernel_version}/extra/thunderx2_pmu-v1.ko

# Load on boot
%{__mkdir_p} %{buildroot}/etc/modules-load.d
%{__cat} << EOF > %{buildroot}/etc/modules-load.d/thunderx2_pmu-v1.conf
# Load thunderx2_pmu-v1 driver at boot
thunderx2_pmu-v1
EOF

%post
/sbin/depmod %{kernel_version}

%files
%attr(0644, root, root) /lib/modules/%{kernel_version}/extra/thunderx2_pmu-v1.ko
%attr(0644, root, root) /etc/modules-load.d/thunderx2_pmu-v1.conf
