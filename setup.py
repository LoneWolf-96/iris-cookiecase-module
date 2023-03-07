from setuptools import setup

setup(
    name='iris-cookiecase-module',
    python_requires='>=3.9',
    version='0.1.0',
    packages=["iris_cookiecase_module"],
    include_package_data=True,
    package_data={'iris_cookiecase_module': ['template/*/*']},
    url='https://github.com/LoneWolf-96/iris-cookiecase-module',
    license='MIT',
    author='iris-cookiecase-module',
    author_email='coding.LoneWolf-96@proton.me',
    description='`iris-cookiecase-module` is a IRIS processor module designed to set out the core note groups and notes required when a new case is created.',
    install_requires=[]
)