'''
from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(

name="Xray",
version="0.0.1",
author="suryakant",
author_email="ssuryakanta696@gmail.com",
#install_requires=get_requirements(r"C:\\Users\\sunny\\deeplearningproject\\requirements_dev.txt"),
install_requires=get_requirements(r"D:\DLPRJ\requirements_dev.txt"),
package=find_packages()

)
'''

from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name="Xray",
    version="0.0.1",
    author="suryakant",
    author_email="ssuryakanta6906@gmail.com",
    install_requires=get_requirements("requirements_dev.txt"),
    packages=find_packages()
)
