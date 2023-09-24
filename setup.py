from setuptools import setup

setup(
    name='qdxcat',
    version='0.2',
    author='Simply Equipped LLC',
    author_email='howard@simplyequipped.com',
    description='Serial CAT control for QRPLabs QDX transceiver',
    packages=setuptools.find_packages(),
    install_requires=['pyserial'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows'
    ]
)

