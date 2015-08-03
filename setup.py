from distutils.core import setup

setup(
    name='pylex',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=['pylex'],
    url='https://github.com/caspervg/pylex',
    license='MIT',
    author='Casper Van Gheluwe',
    author_email='caspervg@gmail.com',
    description='Python wrapper for the SC4Devotion LEX API',
    keywords='lex api wrapper sc4devotion sc4d csxlex bsclex',
    install_requires=['requests>=2.7.0', 'nose>=1.3.7', 'requests-mock>=0.6.0']
)
