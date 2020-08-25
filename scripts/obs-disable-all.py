#!/usr/bin/python

# Disables all packages in a project.
#
# Usage example:
#    obs-disable-all.py --obs https://obs-server --project ATSE:1.2.3
  
import argparse, sys, os, re, time, glob, shlex
from subprocess import Popen, PIPE, STDOUT

parser = argparse.ArgumentParser(description="Disables all packages in a project.")

parser.add_argument('--obs',     type=str, required=True, help ='URL of the OBS server')
parser.add_argument('--project', type=str, required=True, help ='Name of the target project')

args = parser.parse_args()

# Package metadata template
pkgmeta_template = \
"""<package name="@OBSPACKAGENAME@" project="@PROJECT@">
  <title/>
  <description/>
  <build>
    <disable arch="aarch64"/>
    <disable arch="x86_64"/>
    <enable/>
  </build>
</package>"""


# Replaces multiple strings according to the passed in dictionary
def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


# Get the project's list of packages
cmd = "osc -A " + args.obs + " ls " + args.project
tmp = os.popen(cmd).read().rstrip()
packages = re.split("\s+", tmp);
#print packages

# Disable all packages in the target project
for package in packages:
    print "Disabling package", package, "in project", args.project

    keyvals = {
        "@PROJECT@"        : args.project,
        "@OBSPACKAGENAME@" : package
    }

    pkgmeta = multiple_replace(keyvals, pkgmeta_template)

    # Update the package's metadata configuration
    cmd = "osc -A " + args.obs + " meta pkg " + args.project + " " + package + " -F -"
    arg = shlex.split(cmd)
    p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout_data = p.communicate(input=pkgmeta)[0]
    print stdout_data

    cmd = "osc -A https://obs-server api -X POST \"/source/" + args.project + "/" + package + "?cmd=set_flag&flag=build&status=disable\""
    print cmd
    os.system(cmd)
