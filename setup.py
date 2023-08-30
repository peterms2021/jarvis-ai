from setuptools import find_packages, setup

setup(
    name = 'ajarvis-ai',
    version = '0.1',
    description = 'Enterprise Architecture Conversational Agent',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    author = 'ISE Architecture',
    author_email = 'peterwalker@microsoft.com',
    maintainer = 'Peter Walker',
    maintainer_email = 'peterwalker@microsoft.com',
)
