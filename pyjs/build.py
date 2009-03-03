#!/usr/bin/env python

import sys
import os
import shutil
from os.path import join, dirname, basename, abspath, split, isfile, isdir
from optparse import OptionParser

import pyjs



usage = """
  usage: %prog [options] <application module name or path>

This is the command line builder for the pyjamas project, which can be used to
build Ajax applications from Python.
For more information, see the website at http://pyjamas.pyworks.org/
"""

# GWT1.2 Impl  | GWT1.2 Output         | Pyjamas 0.2 Platform | Pyjamas 0.2 Output
# -------------+-----------------------+----------------------+----------------------
# IE6          | ie6                   | IE6                  | ie6
# Opera        | opera                 | Opera                | opera
# Safari       | safari                | Safari               | safari
# --           | gecko1_8              | Mozilla              | mozilla
# --           | gecko                 | OldMoz               | oldmoz
# Standard     | all                   | (default code)       | all
# Mozilla      | gecko1_8, gecko       | --                   | --
# Old          | safari, gecko, opera  | --                   | --

version = "%prog pyjamas version 2006-08-19"
app_platforms = ['IE6', 'Opera', 'OldMoz', 'Safari', 'Mozilla']

app_library_dirs = []
data_dir = dirname(__file__)

def read_boilerplate(filename):
    return open(join(data_dir, "builder/boilerplate", filename)).read()


def copy_boilerplate(filename, output_dir):
    filename = join(data_dir, "builder/boilerplate", filename)
    shutil.copy(filename, output_dir)


# taken and modified from python2.4
def copytree_exists(src, dst, symlinks=False):
    if not os.path.exists(src):
        return

    names = os.listdir(src)
    try:
        os.mkdir(dst)
    except:
        pass

    errors = []
    for name in names:
        if name.startswith('.svn'):
            continue

        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif isdir(srcname):
                copytree_exists(srcname, dstname, symlinks)
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error), why:
            errors.append((srcname, dstname, why))
    if errors:
        print errors


def build(app_name, output="output", js_includes=(), debug=False):
<<<<<<< HEAD:builder/build.py
=======

    dir_public = "public"
>>>>>>> tidyup and shuffle on setup.py.  moved build.py into pyjs/:pyjs/build.py

    # make sure the output directory is always created in the current working
    # directory or at the place given if it is an absolute path.
    output = os.path.abspath(output)

    msg = "Building '%(app_name)s' to output directory '%(output)s'" % locals()
    if debug:
        msg += " with debugging statements"
    print msg

    # check the output directory
    if os.path.exists(output) and not os.path.isdir(output):
        print >>sys.stderr, "Output destination %s exists and is not a directory" % output
        return
    if not os.path.isdir(output):
        try:
            print "Creating output directory"
            os.mkdir(output)
        except StandardError, e:
            print >>sys.stderr, "Exception creating output directory %s: %s" % (output, e)

    ## public dir
    for p in app_library_dirs:
        pub_dir = join(p, 'public')
        if isdir(pub_dir):
            print "Copying: public directory of library %r" % p
            copytree_exists(pub_dir, output)

    ## AppName.html - can be in current or public directory
    html_input_filename = app_name + ".html"
    html_output_filename = join(output, basename(html_input_filename))
    if os.path.isfile(html_input_filename):
        if not os.path.isfile(html_output_filename) or os.path.getmtime(html_input_filename) > os.path.getmtime(html_output_filename):
            try:
                shutil.copy(html_input_filename, html_output_filename)
            except:
                print >>sys.stderr, "Warning: Missing module HTML file %s" % html_input_filename

            print "Copying: %(html_input_filename)s" % locals()

    ## pygwt.js

    print "Copying: pygwt.js"

    pygwt_js_template = read_boilerplate("pygwt.js")
    pygwt_js_output = open(join(output, "pygwt.js"), "w")

    print >>pygwt_js_output, pygwt_js_template

    pygwt_js_output.close()

    ## Images

    print "Copying: Images and History"
    copy_boilerplate("corner_dialog_topleft_black.png", output)
    copy_boilerplate("corner_dialog_topright_black.png", output)
    copy_boilerplate("corner_dialog_bottomright_black.png", output)
    copy_boilerplate("corner_dialog_bottomleft_black.png", output)
    copy_boilerplate("corner_dialog_edge_black.png", output)
    copy_boilerplate("corner_dialog_topleft.png", output)
    copy_boilerplate("corner_dialog_topright.png", output)
    copy_boilerplate("corner_dialog_bottomright.png", output)
    copy_boilerplate("corner_dialog_bottomleft.png", output)
    copy_boilerplate("corner_dialog_edge.png", output)
    copy_boilerplate("tree_closed.gif", output)
    copy_boilerplate("tree_open.gif", output)
    copy_boilerplate("tree_white.gif", output)
    copy_boilerplate("history.html", output)

    ## AppName.nocache.html

    print "Creating: %(app_name)s.nocache.html" % locals()

    home_nocache_html_template = read_boilerplate("home.nocache.html")
    home_nocache_html_output = open(join(output, app_name + ".nocache.html"), "w")

    print >>home_nocache_html_output, home_nocache_html_template % dict(
        app_name = app_name,
        safari_js = "%s.Safari" % app_name,
        ie6_js = "%s.IE6" % app_name,
        oldmoz_js = "%s.OldMoz" % app_name,
        moz_js = "%s.Mozilla" % app_name,
        opera_js = "%s.Opera" % app_name,
    )

    home_nocache_html_output.close()

    ## all.cache.html

    all_cache_html_template = read_boilerplate("all.cache.html")

    parser = pyjs.PlatformParser("platform")
    app_headers = ''
    app_body = '\n'.join(['<script type="text/javascript" src="%s"></script>'%script for script in js_includes])

    for platform in app_platforms:
        all_cache_name = "%s.%s.cache.html" % (app_name, platform)
        print "Creating: " + all_cache_name

        parser.setPlatform(platform)
        app_translator = pyjs.AppTranslator(app_library_dirs, parser)
        app_libs = app_translator.translateLibraries(['pyjslib'], debug)
        app_code = app_translator.translate(app_name, debug=debug)
        all_cache_html_output = open(join(output, all_cache_name), "w")

        print >>all_cache_html_output, all_cache_html_template % dict(
            app_name = app_name,
            app_libs = app_libs,
            app_code = app_code,
            app_body = app_body,
            app_headers = app_headers
        )

        all_cache_html_output.close()

    ## Done.

    print "Done. You can run your app by opening '%(html_output_filename)s' in a browser" % locals()

def main():
    global app_library_dirs
    global app_platforms
    global data_dir

    parser = OptionParser(usage = usage, version = version)
    parser.add_option("-o", "--output", dest="output",
        help="directory to which the webapp should be written")
    parser.add_option("-j", "--include-js", dest="js_includes", action="append",
        help="javascripts to load into the same frame as the rest of the script")
    parser.add_option("-I", "--library_dir", dest="library_dirs",
        action="append", help="path for data directory")
    parser.add_option("-D", "--data_dir", dest="data_dir", 
        help="path for data directory")
    parser.add_option("-P", "--platforms", dest="platforms",
        help="platforms to build for, comma-seperated")
    parser.add_option("-d", "--debug", action="store_true", dest="debug")

    data_dir = os.path.join(sys.prefix, "share/pyjamas")

    parser.set_defaults(output = "output", js_includes=[], library_dirs=[],
                        platforms=(','.join(app_platforms)),
                        data_dir=data_dir,
                        debug=False)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    lib_dirs = set()
    app_path = args[0]
    if app_path.endswith('.py'):
        app_path = abspath(app_path)
        if not isfile(app_path):
            parser.error("Application file not found %r" % app_path)
        app_path, app_name = split(app_path)
        app_name = app_name[:-3]
        lib_dirs.add(app_path)
    elif os.path.sep in app_path:
        parser.error("Not a valid module declaration %r" % app_path)
    else:
        app_name = app_path

    for d in options.library_dirs:
        lib_dirs.add(abspath(d))

    app_library_dirs += tuple(lib_dirs)

    # ok these are the three "default" library directories, containing
    # the builtins (str, List, Dict, ord, round, len, range etc.)
    # the main pyjamas libraries (pyjamas.ui, pyjamas.Window etc.)
    # and the contributed addons
    app_library_dirs += [join(data_dir, "library/builtins"),
                         join(data_dir, "library"),
                         join(data_dir, "addons")]

    if options.platforms:
       app_platforms = options.platforms.split(',')

    # this is mostly for getting boilerplate stuff
    data_dir = os.path.abspath(options.data_dir)

    build(args[0], options.output, options.js_includes,
                   options.debug)
                   

if __name__ == "__main__":
    main()
