from setuptools import setup, find_packages
setup(
    name='verge-python3',
    version='0.1.4',
    description='Friendly VERGE JSON-RPC API binding for Python3',
    long_description='This package allows performing commands such as listing the current balance'
    ' and sending coins to the verge client from Python3. The communication with the'
    ' client happens over JSON-RPC.',
    url='https://github.com/vergecurrency/verge-python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial'
    ],
    packages=find_packages("src"),
	install_requires=['simplejson>=3.8.0'],
    package_dir={'': 'src'}
)
