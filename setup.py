from setuptools import setup

setup(
    name='qdx',
    version='0.1',
    description='QRP Labs QDX tranceiver control library',
    author='Simply Equipped LLC',
    author_email='info@simplyequipped.com',
    packages=['qdx'],
    install_requires=['pyserial', 'flask', 'waitress']
)
