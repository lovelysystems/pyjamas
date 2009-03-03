# Copyright (c) 2007-2008 The PyAMF Project.
# See LICENSE for details.

#from ez_setup import use_setuptools

#use_setuptools()

import glob
from setuptools import setup, find_packages
from setuptools.command import test

import sys
import os

install_requires = []

keyw = """\
"""

lib_data_files = glob.glob("library/*.py")
bp_data_files = glob.glob("builder/boilerplate/*")
build_file = ["builder/build.py"]
pyjs_file = ["pyjs/pyjs.py"]
test_files = glob.glob("pyjs/tests/*")
stub_files = glob.glob("stubs/*")
lib_data_files += glob.glob("library/*.js")
builtin_data_files = glob.glob("library/builtins/*.py")
platform_data_files = glob.glob("library/platform/*.py")
pyjamas_data_files = glob.glob("library/pyjamas/*.py")
addons_data_files = glob.glob("addons/*.py")

data_files = [("/usr/share/pyjamas/library", lib_data_files),
              ("/usr/share/pyjamas/library/builtins", builtin_data_files),
              ("/usr/share/pyjamas/builder/boilerplate", bp_data_files),
              ("/usr/share/pyjamas/pyjs/tests", test_files),
              ("/usr/share/pyjamas/pyjs", pyjs_file),
              ("/usr/share/pyjamas/stubs", stub_files),
              ("/usr/share/pyjamas/builder", build_file),
              ("/usr/share/pyjamas/library/platform", platform_data_files),
              ("/usr/share/pyjamas/library/pyjamas", pyjamas_data_files),
              ("/usr/share/pyjamas/addons", addons_data_files)
              ]

# main purpose of this function is to exclude "output" which
# could have been built by a developer.
def get_files(d):
    res = []
    for p in glob.glob(os.path.join(d, "*")):
        if not p:
            continue
        (pth, fname) = os.path.split(p)
        if fname == "output":
            continue
        if os.path.isdir(p):
            res += get_files(p)
        else:
            res.append(p)
    return res

# ok - examples is a bit of a pain.  

for d in glob.glob("examples/*"):
    if os.path.isdir(d):
        (pth, fname) = os.path.split(d)
        expath = get_files(d)
        pth = os.path.join("/usr/share/pyjamas/examples", fname)
        print pth, expath
        data_files.append((pth, expath))
    else:
        data_files.append(("/usr/share/pyjamas/examples", [d]))
 
from pprint import pprint

pprint(data_files)

if __name__ == '__main__':
    setup(name = "Pyjamas",
        version = "0.4",
        description = "Pyjamas Widget API for Web applications, in Python",
        long_description = open('README', 'rt').read(),
        url = "http://pyjs.org",
        author = "The Pyjamas Project",
        author_email = "lkcl@lkcl.net",
        keywords = keyw,
        scripts = ["bin/pyjscompile", "bin/pyjsbuild"],
        #packages=["pyjamas"],
        install_requires = install_requires,
        data_files = data_files,
        zip_safe=True,
        license = "Apache Software License",
        platforms = ["any"],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Natural Language :: English",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python"
        ])
