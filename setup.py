from setuptools import setup, find_packages

setup(
    name='Data_Science_Python_Module_Model',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='EDSA: Data Science Python Module Package',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'pandas', 'scipy'],
    url='https://github.com/Enyaude/Data_Science_Python_Module_Model.git',
    author='<Enyaude>',
    author_email='<enyaudesamuel@hotmail.com>'
    )