from setuptools import setup, find_packages
import sys

# Check python version
if sys.version_info.major > 2:
    print "Sorry, Python 3 is not yet supported"
    sys.exit(1)

setup(name='obspnts',
      version='0.1',
      packages=find_packages(),
      description='Climate and obsgrid observation IO',
      long_description=('obspnts is Python package that provides a consistent generic '
                        'interface for accessing obsgrid and climate observations '
                        'from multiple different data providers. All station and '
                        'observation data are returned using pandas data structures.'),
      author='Jared W. Oyler',
      author_email='jaredwo@gmail.com',
      license='GPL',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Atmospheric Science',
                   'Topic :: Scientific/Engineering :: GIS',
                   'License :: OSI Approved :: GNU General Public License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7'],
      install_requires=['lxml', 'netCDF4', 'numpy', 'pandas', 'pycurl', 'pytz',
                        'scipy', 'shapely', 'suds', 'tzwhere', 'xray'],
      package_data={'obspnts.providers': ['data/*']}
      )
