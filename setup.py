from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List[str]:

    require = []
    HYPHEN_E_DOT = "-e ." # it refers to setup.py and helps to execute entire code
    
    try:
        with open("requirement.txt","r") as file:
            require = file.readlines()#reading each lines from requirements.txt
            require = [req.replace("\n","") for req in require] #replacing new lines created with no space.
            

            if HYPHEN_E_DOT in require:
                require.remove(HYPHEN_E_DOT)     
                
    except FileNotFoundError:
        print("File doesn't exist..")

    return require

setup(
    author= "Ayushman Mishra",
    name="Network Security",
    version="0.0.1",
    author_email="mishraayush290705@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()

)
    
