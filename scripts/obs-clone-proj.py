#!/usr/bin/python

# Usage example:
#    obs-clone-proj.py --obs https://obs-server --old ATSE:1.2.1 --new ATSE:1.2.1-tx2 --uarch tx2
  
import argparse, sys, os, re, time, glob, shlex
from subprocess import Popen, PIPE, STDOUT

parser = argparse.ArgumentParser(description="Clones an existing OBS project to a new project.")

parser.add_argument('--obs',   type=str, required=True, help ='URL of the OBS server')
parser.add_argument('--old',   type=str, required=True, help ='Name of the old project')
parser.add_argument('--new',   type=str, required=True, help ='Name of the new project')
parser.add_argument('--uarch', type=str, required=True, help ='uarch to use for the new project')

args = parser.parse_args()

#print args.obs
#print args.old
#print args.new
#print args.uarch

# Get the old project's metadata
cmd = "osc -A " + args.obs + " meta prj " + args.old
projmeta = os.popen(cmd).read().rstrip()

# Get the old project's configuration
cmd = "osc -A " + args.obs + " meta prjconf " + args.old
projconf = os.popen(cmd).read().rstrip()

# Update the old project's metadata for the new project name
new_projmeta = re.sub(args.old, args.new, projmeta)
#print new_projmeta

# Get the old project's list of projects
cmd = "osc -A " + args.obs + " ls " + args.old
tmp = os.popen(cmd).read().rstrip()
packages = re.split("\s+", tmp);
#print packages

# Auto-create the new project by adding its metadata configuration
cmd = "osc -A " + args.obs + " meta prj " + args.new + " -F -"
arg = shlex.split(cmd)
p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
stdout_data = p.communicate(input=new_projmeta)[0]
print stdout_data

# Copy the old project's configuration to the new project
cmd = "osc -A " + args.obs + " meta prjconf " + args.new + " -F -"
arg = shlex.split(cmd)
p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
stdout_data = p.communicate(input=projconf)[0]
print stdout_data

# Copy all packages to the new project
for package in packages:
    print "Creating package", package, "in project", args.new

    # Get the package's metadata from the old project
    cmd = "osc -A " + args.obs + " meta pkg " + args.old + " " + package
    pkgmeta = os.popen(cmd).read().rstrip()

    # Update the package's metadata for the new project
    new_pkgmeta = re.sub(args.old, args.new, pkgmeta)

    # Create the package in the new project
    cmd = "osc -A " + args.obs + " meta pkg " + args.new + " " + package + " -F -"
    arg = shlex.split(cmd)
    p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout_data = p.communicate(input=new_pkgmeta)[0]
    print stdout_data


# Go through each package and add a link from the new project to the old project,
# tacking on a uarch=foo to the top of each spec file.
for package in packages:
    print "Linking package", package

    cmd = "osc -A " + args.obs + " checkout --unexpand-link " + args.new + " " + package
    print cmd
    os.system(cmd)

    file = open(args.new + "/" + package + "/_link", "w")
    file.write("<link project='" + args.old + "' package='" + package + "'>\n")
    file.write("<patches>\n")
    file.write("  <topadd>%define uarch " + args.uarch + "</topadd>\n")
    file.write("</patches>\n")
    file.write("</link>\n")
    file.close()

    cmd = "osc -A " + args.obs + " add " + args.new + "/" + package + "/_link"
    print cmd
    os.system(cmd)

# Commit everything
os.chdir(args.new)
cmd = "osc -A " + args.obs + " ci -m \"initial commit\""
print cmd
os.system(cmd)
