## tips for including PyAlchemy taken from http://japrogbits.blogspot.com.es/2010/07/py2exe-and-sqlalchemy.html

from distutils.core import setup
import py2exe #@UnusedImport
import platform
 
# 1. List of python modules to exclude from the distribution
mod_excludes = [
    "Tkinter",
    "doctest",
    "unittest",
    "pydoc",
    "pygments",
    "pdb",
    "email"
]
 
# 2. List of dll's (and apparently exe's) to exclude from the distribution
#    if any Windows system dll appears in the dist folder, add it to this
#    list.
dll_excludes = [
    "API-MS-Win-Core-LocalRegistry-L1-1-0.dll",
    "POWRPROF.dll",
    "w9xpopen.exe"
]
 
# 3. List of python modules that are to be manually included.
mod_includes = [
    "Cheetah.DummyTransaction",
]
 
# 4. List of python packages that are to be manually included.
package_includes = [
    "sqlite3",
    "sqlalchemy.dialects.sqlite"
]

# 5. determine the distribution folder.
arch = platform.architecture()
if '32bit' in arch:
    dist_dir = "dist-x86"
elif '64bit' in arch:
    dist_dir = "dist-x64"
else:
    raise RuntimeError("Unsupported architecture!")
 
# 6. Dictionary of options to pass to py2exe
py2exe_options = {
    "optimize": 2, # 0 (None), 1 (-O), 2 (-OO)
    "includes": mod_includes,
    "excludes": mod_excludes,
    "dll_excludes": dll_excludes,
    "packages": package_includes,
    "xref": False,
    # bundle_files: 1|2|3
    #    1: executable and library.zip
    #    2: executable, Python DLL, library.zip
    #    3: executable, Python DLL, other DLLs and PYDs, library.zip
    "bundle_files": 3,
    "dist_dir": dist_dir
}
 
# 7. call setup to create the service and the console app
setup(service=[{'modules': 'myservice',
                'icon_resources': [(1, '..\\my.ico')]
               }],
      console=[{'script': '..\\myexe.py',
                'icon_resources': [(1, '..\\my.ico')]
              }],
      version='1.0',
      description='My Service',
      long_description="My service verbose description.",
      author='Jon Anglin',
      author_email='jonanglin@somewhere.com',
      url='http://japrogbits.blogspot.com',
      options={"py2exe": py2exe_options}
     )