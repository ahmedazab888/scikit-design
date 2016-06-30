#!/usr/bin/env python
import os
import sys
import subprocess
from setuptools import setup

descr = """\
Scikit-Design

Tools for statistical study design for clinical trials, qualtiy control, etc.
"""

DISTNAME            = 'scikit-learn'
DESCRIPTION         = 'Tools for Statistical Study Design'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Christopher Louden',
MAINTAINER_EMAIL    = 'loudenconsulting@gmail.com',
URL                 = 'http://github.com/louden/scikit-design'
LICENSE             = 'MIT'
DOWNLOAD_URL        = URL
PACKAGE_NAME        = 'skdesign'
EXTRA_INFO          = dict(
    install_requires=['scipy'],
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Scientific/Engineering']
)


def get_version():
    """Obtain the version number"""
    import imp
    mod = imp.load_source('version', os.path.join(PACKAGE_NAME, 'version.py'))
    return mod.__version__

# Documentation building command
try:
    from sphinx.setup_command import BuildDoc as SphinxBuildDoc

    class BuildDoc(SphinxBuildDoc):
        """Run in-place build before Sphinx doc build"""
        def run(self):
            ret = subprocess.call([sys.executable, sys.argv[0],
                                   'build_ext', '-i'])
            if ret != 0:
                raise RuntimeError("Building Scipy failed!")
            SphinxBuildDoc.run(self)
    cmdclass = {'build_sphinx': BuildDoc}
except ImportError:
    cmdclass = {}

# Call the setup function
if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          include_package_data=True,
          test_suite="py.test",
          # cmdclass=cmdclass,
          version=get_version())
