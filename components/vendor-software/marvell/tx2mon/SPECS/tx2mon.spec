#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the ATSE project.
#----------------------------------------------------------------------------eh-

# Define the kernel version to build tx2mon_kmod.ko against.
# This is the output of `uname -r` on the target system.
%define kernel_version 4.14.0-115.el7a.aarch64

%define pname tx2mon

%include %{_sourcedir}/OHPC_macros

Summary:     Top-like monitor for the Marvell ThunderX2 System on a Chip
Name:        %{pname}%{PROJ_DELIM}
Version:     20191029
Release:     1%{?dist}
License:     GPLv2
Group:       %{PROJ_NAME}/tools
URL:         https://github.com/jchandra-cavm/tx2mon
Source0:     %{pname}-%{version}.tar.gz
ExcludeArch: x86_64

BuildRequires: gcc
BuildRequires: kernel
BuildRequires: kernel-devel
BuildRequires: ncurses-devel
Requires: kernel
Requires: ncurses

%description
Top-like monitor for the Marvell ThunderX2 System on a Chip.

%prep
%setup -n %{pname}-%{version}

%build

# Build the tx2mon kernel module
cd modules
sed -i 's/\$(shell uname -r)/%{kernel_version}/g' Makefile
make
cd ..

# Build the user-space utility
cd tx2mon
make
cd ..

%install
# Install the tx2mon kernel module
%{__mkdir_p} %{buildroot}/lib/modules/%{kernel_version}/extra
cp modules/tx2mon_kmod.ko %{buildroot}/lib/modules/%{kernel_version}/extra/tx2mon_kmod.ko

# Install the tx2mon user utility
%{__mkdir_p} %{buildroot}/usr/bin
cp tx2mon/tx2mon %{buildroot}/usr/bin/tx2mon

%{__mkdir_p} %{buildroot}/usr/include/tx2mon
cp tx2mon/mc_oper_region.h %{buildroot}/usr/include/tx2mon/mc_oper_region.h

# Load on boot
%{__mkdir_p} %{buildroot}/etc/modules-load.d
%{__cat} << EOF > %{buildroot}/etc/modules-load.d/tx2mon_kmod.conf
# Load tx2mon driver at boot
tx2mon_kmod
EOF

# Set permissions on boot
%{__mkdir_p} %{buildroot}/etc/systemd/system
%{__cat} << EOF > %{buildroot}/etc/systemd/system/tx2mon-permissions.service
[Unit]
Description=tx2mon sysfs permissions
After=systemd-modules-load.service

[Service]
Type=oneshot
User=root
ExecStart=/bin/bash -c "/bin/chmod go+r /sys/bus/platform/devices/tx2mon/node*_raw"

[Install]
WantedBy=multi-user.target
EOF

%post
/sbin/depmod %{kernel_version}
#/sbin/modprobe tx2mon_kmod
#/bin/systemctl daemon-reload
/bin/systemctl enable tx2mon-permissions.service
#/bin/systemctl start  tx2mon-permissions.service

#%preun
#/sbin/rmmod tx2mon_kmod

#%postun
#/bin/systemctl daemon-reload

%files
%attr(0644, root, root) /lib/modules/%{kernel_version}/extra/tx2mon_kmod.ko
%attr(0644, root, root) /etc/modules-load.d/tx2mon_kmod.conf
%attr(0644, root, root) /etc/systemd/system/tx2mon-permissions.service
%attr(0755, root, root) /usr/bin/tx2mon
%attr(0644, root, root) /usr/include/tx2mon/mc_oper_region.h
