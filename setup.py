from setuptools import setup, find_packages

setup(
    name='Python_Module_for_Data_Science',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='EDSA: Python module for data science package',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'pandas', 'scipy'],
    url='https://github.com/Enyaude/Python_Module_for_Data_Science.git',
    author='<Enyaude>',
    author_email='<enyaudesamuel@hotmail.com>'
    )