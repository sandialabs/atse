#!/usr/bin/python

# Example,  run in a freshly created directory:
#
# ../scripts/obs-build-atse-proj.py --obs https://obs-server --version 1.2.4 --atsedir /atse
  
import argparse, sys, os, re, time, glob, shlex
from subprocess import Popen, PIPE, STDOUT

##############################################################################
# Start of templates
##############################################################################

# Project MetaData
projmeta_template = \
"""<project name="ATSE:@VERSION@">
  <title>ATSE Version @VERSION@</title>
  <description/>
  <person userid="Admin" role="maintainer"/>
  <build>
    <enable arch="aarch64"/>
    <enable arch="x86_64"/>
    <enable/>
  </build>
  <publish>
    <enable/>
  </publish>
  <repository name="RHEL_7.6">
    <path project="NonFree:MOFED:4.7-3.2.9.0" repository="RHEL_7.6"/>
    <path project="RHEL" repository="7.6"/>
    <path project="EPEL7-deps" repository="standard"/>
    <path project="NonFree:ArmHPC:20.1" repository="RHEL_7.6"/>
    <path project="NonFree:HPE-MPI:1.4" repository="RHEL_7.6"/>
    <arch>aarch64</arch>
    <arch>x86_64</arch>
  </repository>
</project>"""

# Project Configuration
projconf_template = \
"""# Add release tag attribute
Release: <CI_CNT>.<B_CNT>.atse.@VERSION@

Prefer: gnu-free-sans-fonts
Prefer: infinipath-psm
Prefer: postgresql96-server
Prefer: libibmad
Prefer: perl
Prefer: libtool-atse
Prefer: hwloc-atse
Prefer: mlnx-ofa_kernel-devel
Prefer: libwayland-egl
Prefer: elinks

Preinstall: findutils
Preinstall: systemd-libs
Preinstall: procps-ng

%if 0%{?rhel_version} || 0%{?centos_version}
Preinstall: perl-Exporter
Preinstall: perl-Data-Dumper
Preinstall: perl-Carp
Preinstall: perl-Getopt-Long
Preinstall: perl-constant
Preinstall: perl-Digest-MD5
Patterntype: comps
%endif

Macros:
%OHPC_BUILD 1"""

# Package metadata template
pkgmeta_template = \
"""<package name="@OBSPACKAGENAME@" project="ATSE:@VERSION@">
  <title/>
  <description/>
  <build>
    <enable arch="aarch64"/>
    <enable arch="x86_64"/>
    <enable/>
  </build>
</package>"""

# Package metadata template
pkgmeta_arm_only_template = \
"""<package name="@OBSPACKAGENAME@" project="ATSE:@VERSION@">
  <title/>
  <description/>
  <build>
    <enable arch="aarch64"/>
    <disable arch="x86_64"/>
    <enable/>
  </build>
</package>"""

# Package _service file template
service_template = \
"""<services>

  <service name="tar_scm">

    <!-- Begin INPUT ######################################  -->
    <!--    Update following lines to define the             -->
    <!--    correct component path in git and desired branch -->

    <param name="subdir">components</param>
    <param name="revision">@VERSION@</param>
    <param name="include">@GITDIR@</param>
    <param name="include">OHPC_macros</param>
    <param name="include">ATSE_setup_compiler</param>
    <param name="include">ATSE_setup_mpi</param>

    <!-- End INPUT ######################################    -->

    <param name="scm">git</param>
    <param name="url">https://atse.sandia.gov/atse/atse.git</param>
    <param name="filename">git-infra</param>
    <param name="changesgenerate">enable</param>

  </service>

  <service name="extract_file">

    <!-- Begin INPUT 2 ####################################  -->
    <!--    Update the following lines to define files to    -->
    <!--    extract for package tarball                      -->

    <param name="files">
      */@BASEDIR@/@PACKAGENAME@/SPECS/*.spec
      */@BASEDIR@/@PACKAGENAME@/SOURCES/*
      */OHPC_macros
      */ATSE_setup_compiler
      */ATSE_setup_mpi
    </param>

    <!-- End INPUT 2 ###################################### -->

    <param name="archive">*.tar</param>
  </service>

</services>"""

# Package _link file template for compiler dependent packages
# The "gnu7" target is the base package, by convention
link_compiler_template = \
"""<link project='ATSE:@VERSION@' package='@PACKAGENAME@-gnu7'>
<patches>
  <topadd>%define compiler_family @COMPILER@</topadd>
</patches>
</link>"""

# Package _link file template for compiler and mpi dependent packages
# The "gnu7-openmpi3" target is the base package, by convention
link_mpi_template = \
"""<link project='ATSE:@VERSION@' package='@PACKAGENAME@-gnu7-openmpi3'>
<patches>
  <topadd>%define compiler_family @COMPILER@</topadd>
  <topadd>%define mpi_family @MPI@</topadd>
</patches>
</link>"""


##############################################################################
# End of templates
##############################################################################

##############################################################################
# Start of helper functions
##############################################################################


# Replaces multiple strings according to the passed in dictionary
def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


# Adds a project to the OBS project using a full _service file
def add_package_service(keyvals):

  # Build package-specific config files from templates
  pkgmeta = multiple_replace(keyvals, pkgmeta_template)
  service = multiple_replace(keyvals, service_template)

  pkgname = keyvals["@OBSPACKAGENAME@"]
  print "Adding ", pkgname, "..."

  # Auto-create the new package by adding its metadata configuration
  cmd = "osc -A " + args.obs + " meta pkg " + projname + " " + pkgname + " -F -"
  arg = shlex.split(cmd)
  p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  stdout_data = p.communicate(input=pkgmeta)[0]
  print stdout_data

  # Checkout the new package
  cmd = "osc -A " + args.obs + " checkout --unexpand-link " + projname + " " + pkgname
  print cmd
  os.system(cmd)

  # Populate the _service file
  file = open(projname + "/" + pkgname + "/_service", "w")
  file.write(service)
  file.close()

  # Add the _service file to the package
  cmd = "osc -A " + args.obs + " add " + projname + "/" + pkgname + "/_service"
  print cmd
  os.system(cmd)

  # Add external source files
  for filename in keyvals["FILES"]:
    src = args.atsedir + "/components/" + keyvals["@BASEDIR@"] + "/" + keyvals["@PACKAGENAME@"] + "/SOURCES/" + filename
    dst = projname + "/" + pkgname + "/" + filename
    cmd = "cp " + src + " " + dst
    print cmd
    os.system(cmd)

    cmd = "osc -A " + args.obs + " add " + dst
    os.system(cmd)
    os.system(cmd)

  print "    DONE."


# Adds a project to the OBS project using an OBS _link file
def add_package_link(keyvals, link):

  # Build package-specific config files from templates
  if keyvals["@COMPILER@"] == "gnu9" or keyvals["@COMPILER@"] == "arm" or keyvals["@MPI@"] == "hpempi":
      pkgmeta = multiple_replace(keyvals, pkgmeta_arm_only_template)
  else:
      pkgmeta = multiple_replace(keyvals, pkgmeta_template)

  pkgname = keyvals["@OBSPACKAGENAME@"]
  print "Adding ", pkgname, "..."

  # Auto-create the new package by adding its metadata configuration
  cmd = "osc -A " + args.obs + " meta pkg " + projname + " " + pkgname + " -F -"
  arg = shlex.split(cmd)
  p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  stdout_data = p.communicate(input=pkgmeta)[0]
  print stdout_data

  # Checkout the new package
  cmd = "osc -A " + args.obs + " checkout --unexpand-link " + projname + " " + pkgname
  print cmd
  os.system(cmd)

  # Populate the _link file
  file = open(projname + "/" + pkgname + "/_link", "w")
  file.write(link)
  file.close()

  # Add the _link file to the package
  cmd = "osc -A " + args.obs + " add " + projname + "/" + pkgname + "/_link"
  print cmd
  os.system(cmd)

  print "    DONE."


# Populates a new package
def add_package(keyvals):

  # Set GITDIR derived keyval, needed for the service_template
  gitdir = re.sub("/.*", "", keyvals["@BASEDIR@"])
  keyvals["@GITDIR@"] = re.sub("-", "[-]", gitdir)

  # Determine if the package is compiler and/or mpi dependent
  compiler_dependent = True if len(keyvals["COMPILERS"]) else False
  mpi_dependent      = True if len(keyvals["MPIS"])      else False

  if compiler_dependent == False and mpi_dependent == False:
    # Package is only dependent on base OS compiler and libraries
    keyvals["@OBSPACKAGENAME@"] = keyvals["@PACKAGENAME@"]
    add_package_service(keyvals)

  elif compiler_dependent == True and mpi_dependent == False:
    # Package is dependent on ATSE compilers only

    # Step 1, build the base gnu7 package
    keyvals["@OBSPACKAGENAME@"] = keyvals["@PACKAGENAME@"] + "-gnu7"
    add_package_service(keyvals)

    # Step 2, link each additional compiler variant to the base gnu7 package 
    for compiler in keyvals["COMPILERS"]:
      if compiler == "gnu7":
        continue
      keyvals["@OBSPACKAGENAME@"] = keyvals["@PACKAGENAME@"] + "-" + compiler
      keyvals["@COMPILER@"]       = compiler
      link = multiple_replace(keyvals, link_compiler_template)
      add_package_link(keyvals, link)

  elif compiler_dependent == True and mpi_dependent == True:
    # Package is dependent on ATSE compilers and ATSE MPIs 

    # Step 1, build the base gnu7-openmpi3 package
    keyvals["@OBSPACKAGENAME@"] = keyvals["@PACKAGENAME@"] + "-gnu7-openmpi3"
    add_package_service(keyvals)

    # Step 2, link each additional compiler variant to the base gnu7-openmpi3 package 
    for compiler in keyvals["COMPILERS"]:
      for mpi in keyvals["MPIS"]:
        if ((compiler == "gnu7") and (mpi == "openmpi3")):
          continue
        keyvals["@OBSPACKAGENAME@"] = keyvals["@PACKAGENAME@"] + "-" + compiler + "-" + mpi
        keyvals["@COMPILER@"]       = compiler
        keyvals["@MPI@"]            = mpi
        link = multiple_replace(keyvals, link_mpi_template)
        add_package_link(keyvals, link)


##############################################################################
# End of helper functions
##############################################################################

##############################################################################
# Start of main
##############################################################################

parser = argparse.ArgumentParser(description="Creates an OBS project for ATSE.")

parser.add_argument('--obs',     type=str, required=True, help ='URL of the OBS server')
parser.add_argument('--version', type=str, required=True, help ='Version of the new ATSE project')
parser.add_argument('--atsedir', type=str, required=True, help ='Base directory to ATSE git repo')

args = parser.parse_args()

print args.obs
print args.version
print args.atsedir

projname = "ATSE:" + args.version
print projname


# Update the project metadata and conf for the target ATSE version number
projmeta = re.sub("@VERSION@", args.version, projmeta_template)
projconf = re.sub("@VERSION@", args.version, projconf_template)

#print projmeta
#print projconf

# Auto-create the new project by adding its metadata configuration
cmd = "osc -A " + args.obs + " meta prj " + projname + " -F -"
arg = shlex.split(cmd)
p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
stdout_data = p.communicate(input=projmeta)[0]
print stdout_data

# Populate the new project's prjconf
cmd = "osc -A " + args.obs + " meta prjconf " + projname + " -F -"
arg = shlex.split(cmd)
p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
stdout_data = p.communicate(input=projconf)[0]
print stdout_data

##############################################################################
# Common package config
##############################################################################
keyvals = {
  "@VERSION@" : args.version
}

##############################################################################
# lua-bit
##############################################################################
keyvals["@PACKAGENAME@"] = "lua-bit"
keyvals["@BASEDIR@"]     = "distro-packages"
keyvals["FILES"]         = ["LuaBitOp-1.0.2.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# lua-posix
##############################################################################
keyvals["@PACKAGENAME@"] = "lua-posix"
keyvals["@BASEDIR@"]     = "distro-packages"
keyvals["FILES"]         = ["release-v33.2.1.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# lua-filesystem
##############################################################################
keyvals["@PACKAGENAME@"] = "lua-filesystem"
keyvals["@BASEDIR@"]     = "distro-packages"
keyvals["FILES"]         = ["v_1_6_3.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# atse-filesystem
##############################################################################
keyvals["@PACKAGENAME@"] = "atse-filesystem"
keyvals["@BASEDIR@"]     = "admin"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# atse-buildroot
##############################################################################
keyvals["@PACKAGENAME@"] = "atse-buildroot"
keyvals["@BASEDIR@"]     = "admin"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# lmod
##############################################################################
keyvals["@PACKAGENAME@"] = "lmod"
keyvals["@BASEDIR@"]     = "admin"
keyvals["FILES"]         = ["7.8.1.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# ovis
##############################################################################
keyvals["@PACKAGENAME@"] = "ovis"
keyvals["@BASEDIR@"]     = "admin"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# ldms
##############################################################################
keyvals["@PACKAGENAME@"] = "ldms"
keyvals["@BASEDIR@"]     = "admin"
keyvals["FILES"]         = ["ovis-ldms-4.3.3.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# autoconf
##############################################################################
keyvals["@PACKAGENAME@"] = "autoconf"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["autoconf-2.69.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# automake
##############################################################################
keyvals["@PACKAGENAME@"] = "automake"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["automake-1.16.1.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# libtool
##############################################################################
keyvals["@PACKAGENAME@"] = "libtool"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["libtool-2.4.6.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# ninja
##############################################################################
keyvals["@PACKAGENAME@"] = "ninja"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["v1.8.2.g81279.kitware.dyndep-1.jobserver-1.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# cmake
##############################################################################
keyvals["@PACKAGENAME@"] = "cmake"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["cmake-3.17.1.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# cmake-3.9
##############################################################################
keyvals["@PACKAGENAME@"] = "cmake-3.9"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["cmake-3.9.2.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# cmake-3.14.5
##############################################################################
keyvals["@PACKAGENAME@"] = "cmake-3.14.5"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["cmake-3.14.5.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# git
##############################################################################
keyvals["@PACKAGENAME@"] = "git"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["git-2.26.2.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# git-lfs
##############################################################################
keyvals["@PACKAGENAME@"] = "git-lfs"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["git-lfs-2.10.0.tar.gz", "git-lfs-2.10.0-aarch64", "git-lfs-2.10.0-x86_64"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# spack
##############################################################################
keyvals["@PACKAGENAME@"] = "spack"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["spack-0.14.2.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# valgrind
##############################################################################
keyvals["@PACKAGENAME@"] = "valgrind"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["valgrind-20200315.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# singularity
##############################################################################
keyvals["@PACKAGENAME@"] = "singularity"
keyvals["@BASEDIR@"]     = "container-runtimes"
keyvals["FILES"]         = ["singularity-3.5.3.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# charliecloud
##############################################################################
keyvals["@PACKAGENAME@"] = "charliecloud"
keyvals["@BASEDIR@"]     = "container-runtimes"
keyvals["FILES"]         = ["charliecloud-0.15.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# pmix
##############################################################################
keyvals["@PACKAGENAME@"] = "pmix"
keyvals["@BASEDIR@"]     = "rms"
keyvals["FILES"]         = ["pmix-2.2.3.tar.bz2"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# munge
##############################################################################
keyvals["@PACKAGENAME@"] = "munge"
keyvals["@BASEDIR@"]     = "rms"
keyvals["FILES"]         = ["munge-0.5.13.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# slurm
##############################################################################
keyvals["@PACKAGENAME@"] = "slurm"
keyvals["@BASEDIR@"]     = "rms"
keyvals["FILES"]         = ["slurm-19.05.5.tar.bz2"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# binutils
##############################################################################
keyvals["@PACKAGENAME@"] = "binutils"
keyvals["@BASEDIR@"]     = "compiler-families"
keyvals["FILES"]         = ["binutils-2.33.1.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# gnu7 compilers
##############################################################################
keyvals["@PACKAGENAME@"] = "gnu-compilers"
keyvals["@BASEDIR@"]     = "compiler-families"
keyvals["FILES"]         = ["gmp-6.1.2.tar.bz2", "mpc-1.1.0.tar.gz", "mpfr-4.0.1.tar.gz", "isl-0.18.tar.bz2", "gcc-7.2.0.tar.xz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# gnu9 compilers
##############################################################################
keyvals["@PACKAGENAME@"] = "gnu9-compilers"
keyvals["@BASEDIR@"]     = "compiler-families"
keyvals["FILES"]         = ["gmp-6.1.0.tar.bz2", "mpfr-3.1.4.tar.bz2", "mpc-1.0.3.tar.gz", "isl-0.18.tar.bz2", "gcc-9.3.0.tar.xz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# arm compilers
##############################################################################
keyvals["@PACKAGENAME@"] = "arm-compilers"
keyvals["@BASEDIR@"]     = "compiler-families"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# arm-licenses
##############################################################################
keyvals["@PACKAGENAME@"] = "arm-licenses"
keyvals["@BASEDIR@"]     = "admin/licenses"
keyvals["FILES"]         = ["arm-compiler-for-hpc-snl"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# gdb
##############################################################################
keyvals["@PACKAGENAME@"] = "gdb"
keyvals["@BASEDIR@"]     = "debuggers"
keyvals["FILES"]         = ["gmp-6.1.2.tar.bz2", "mpc-1.1.0.tar.gz", "mpfr-4.0.1.tar.gz", "isl-0.18.tar.bz2", "gdb-8.2.tar.xz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# armpl [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "armpl"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# zlib [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "zlib"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["zlib-1.2.11.tar.xz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# bzip2 [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "bzip2"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["bzip2-1.0.6.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# xz [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "xz"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["xz-5.2.4.tar.xz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# yaml-cpp [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "yaml-cpp"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["yaml-cpp-0.6.2.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# numactl [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "numactl"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["numactl-2.0.12.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# hwloc [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "hwloc"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["hwloc-1.11.11.tar.bz2"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# openblas [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "openblas"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["v0.3.4.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# superlu [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "superlu"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["superlu_5.2.1.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# metis [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "metis"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["metis-5.1.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# scotch [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "scotch"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["scotch_6.0.6.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# papi [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "papi"
keyvals["@BASEDIR@"]     = "perf-tools"
keyvals["FILES"]         = ["papi-5.7.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# qthreads [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "qthreads"
keyvals["@BASEDIR@"]     = "runtime-systems"
keyvals["FILES"]         = ["qthreads-1.14.tar.bz2"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# openucx [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "openucx"
keyvals["@BASEDIR@"]     = "net-libs"
keyvals["FILES"]         = ["ucx-1.7.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# openmpi3 [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "openmpi3"
keyvals["@BASEDIR@"]     = "mpi-families"
keyvals["FILES"]         = ["openmpi-3.1.4.tar.bz2"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# openmpi4 [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "openmpi4"
keyvals["@BASEDIR@"]     = "mpi-families"
keyvals["FILES"]         = ["openmpi-4.0.3.tar.bz2"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# hpempi [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "hpempi"
keyvals["@BASEDIR@"]     = "mpi-families"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# hello [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "hello"
keyvals["@BASEDIR@"]     = "dev-tools"
keyvals["FILES"]         = ["hello-1.0.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

#============================================================================
# 
# Start of I/O Libraries
#
#============================================================================

##############################################################################
# hdf5 [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "hdf5"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["hdf5-1.10.5.tar.bz2"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# phdf5 [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "phdf5"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["hdf5-1.10.5.tar.bz2"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# netcdf [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "netcdf"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["v4.6.3.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# netcdf-cxx [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "netcdf-cxx"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["v4.3.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# netcdf-fortran [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "netcdf-fortran"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["v4.4.5.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# pnetcdf [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "pnetcdf"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["pnetcdf-1.11.1.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

#============================================================================
# 
# End of I/O Libraries
#
#============================================================================

##############################################################################
# fftw [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "fftw"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["fftw-3.3.8.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# ptscotch [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "ptscotch"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["scotch_6.0.6.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# parmetis [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "parmetis"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["parmetis-4.0.3.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# superlu_dist [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "superlu_dist"
keyvals["@BASEDIR@"]     = "math-libs"
keyvals["FILES"]         = ["superlu_dist_5.4.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# boost [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "boost"
keyvals["@BASEDIR@"]     = "parallel-libs"
keyvals["FILES"]         = ["boost_1_72_0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# cgns [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "cgns"
keyvals["@BASEDIR@"]     = "io-libs"
keyvals["FILES"]         = ["v3.4.0.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# mpiP [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "mpiP"
keyvals["@BASEDIR@"]     = "perf-tools"
keyvals["FILES"]         = ["mpiP-3.4.1.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# imb [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "imb"
keyvals["@BASEDIR@"]     = "perf-tools"
keyvals["FILES"]         = ["v2018.1.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# omb [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "omb"
keyvals["@BASEDIR@"]     = "perf-tools"
keyvals["FILES"]         = ["osu-micro-benchmarks-5.6.1.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# pdtoolkit [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "pdtoolkit"
keyvals["@BASEDIR@"]     = "perf-tools"
keyvals["FILES"]         = ["pdtoolkit-3.25.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# powerapi [compiler dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "powerapi"
keyvals["@BASEDIR@"]     = "util-libs"
keyvals["FILES"]         = ["powerapi-20200529.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# tau [compiler dependent] [mpi dependent]
##############################################################################
keyvals["@PACKAGENAME@"] = "tau"
keyvals["@BASEDIR@"]     = "perf-tools"
keyvals["FILES"]         = ["tau-2.28.tar.gz"]
keyvals["COMPILERS"]     = ["gnu7", "arm"]
keyvals["MPIS"]          = ["openmpi3", "openmpi4", "hpempi"]
add_package(keyvals)

##############################################################################
# devpacks
##############################################################################
keyvals["@PACKAGENAME@"] = "devpacks"
keyvals["@BASEDIR@"]     = "admin"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# tx2mon
##############################################################################
keyvals["@PACKAGENAME@"] = "tx2mon"
keyvals["@BASEDIR@"]     = "vendor-software/marvell"
keyvals["FILES"]         = ["tx2mon-20191029.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# tx2pmu
##############################################################################
keyvals["@PACKAGENAME@"] = "tx2pmu"
keyvals["@BASEDIR@"]     = "vendor-software/marvell"
keyvals["FILES"]         = ["tx2pmu-20191029.tar.gz"]
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

##############################################################################
# arm-tools-modulefiles
##############################################################################
keyvals["@PACKAGENAME@"] = "arm-tools-modulefiles"
keyvals["@BASEDIR@"]     = "vendor-software/arm"
keyvals["FILES"]         = []
keyvals["COMPILERS"]     = []
keyvals["MPIS"]          = []
add_package(keyvals)

# Commit everything
os.chdir(projname)
cmd = "osc -A " + args.obs + " ci -m \"initial commit\""
print cmd
os.system(cmd)
