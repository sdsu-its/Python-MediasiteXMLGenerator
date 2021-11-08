from setuptools import setup

setup(
    name='mediasiteXMLGen',
    url='https://github.com/sdsu-its/mediasiteXMLGen',
    author='Mirza Ishraq Yeahia',
    author_email='myeahia@sdsu.edu',
    packages=['mediasiteXMLGen'],
    install_requires=['numpy','pandas','lxml','setuptools','minidom-ext'],
    version='0.1',
    license='MIT',
    description='A tool to generate Mediasite recording schedule.',
)