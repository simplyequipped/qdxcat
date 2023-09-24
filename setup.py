from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='qdxcat',
    version='0.2.0',
    author='Simply Equipped LLC',
    author_email='howard@simplyequipped.com',
    description='Serial CAT control for QRPLabs QDX transceiver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simplyequipped/qdxcat',
    packages=setuptools.find_packages(),
    install_requires=['pyserial'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows'
    ],
    python_requires='>=3.6'
)

