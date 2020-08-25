%include %{_sourcedir}/OHPC_macros

Name:       arm-licenses-snl%{PROJ_DELIM}
Version:    1
Release:    1%{?dist}
Summary:    SNL licenses for Arm software products

Group:      Licenses
License:    None
URL:        https://developer.arm.com
Source0:    arm-compiler-for-hpc-snl

BuildArch:  noarch

Provides:   arm-licenses
Conflicts:  arm-licenses

%description
SNL licenses for Arm software products.  These are not the actual licenses,
rather the config files needed to access the SNL site license server.

%install
mkdir -p %{buildroot}/opt/arm/licenses
install -p -m 644 %{SOURCE0} %{buildroot}/opt/arm/licenses/License

%files
/opt/arm/licenses
