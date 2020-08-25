%global pname arm-tools-modulefiles

%include %{_sourcedir}/OHPC_macros

Summary:     Module files for Arm Forge and Reports tools
Name:        %{pname}%{PROJ_DELIM}
Version:     20.0.2
Release:     1%{?dist}
License:     Apache-2.0
URL:         https://github.com/openhpc/ohpc
Group:       %{PROJ_NAME}/math-libs

%description
Module files for interfacing ATSE with the Arm Forge and Reports tools.

%install

# Forge modulefile
%{__mkdir_p} %{buildroot}%{OHPC_MODULES}/forge
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/forge/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Arm Allinea Forge tools."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: Forge"
module-whatis "Version: %{version}"
module-whatis "Category: utility, developer support"
module-whatis "Keywords: System, Utility"
module-whatis "Description: Arm Allinea Forge DDT Debugger and MAP Profiler"

set             version                 %{version}

set             prefix                  /opt/arm/forge/%{version}

prepend-path    PATH                    \$prefix/bin
EOF


# Reports modulefile
%{__mkdir_p} %{buildroot}%{OHPC_MODULES}/reports
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/reports/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Arm Allinea Reports tools."
puts stderr "\nVersion %{version}\n"

}

module-whatis "Name: Reports"
module-whatis "Version: %{version}"
module-whatis "Category: utility, developer support"
module-whatis "Keywords: System, Utility"
module-whatis "Description: Arm Allinea Reports tools"

set             version                 %{version}

set             prefix                  /opt/arm/reports/%{version}

prepend-path    PATH                    \$prefix/bin
EOF

%files
%{OHPC_PUB}
