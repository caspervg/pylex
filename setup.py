from distutils.core import setup

setup(
    name='lex4py',
    version='1.1.2',
    package_dir={'': 'src'},
    packages=['pylex'],
    url='https://github.com/caspervg/pylex',
    license='MIT',
    author='Casper Van Gheluwe',
    author_email='caspervg@gmail.com',
    description='Python wrapper for the SC4Devotion LEX API',
    keywords='lex api wrapper sc4devotion sc4d csxlex bsclex',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['requests>=2.7.0', 'nose>=1.3.7', 'requests-mock>=0.6.0']
)
