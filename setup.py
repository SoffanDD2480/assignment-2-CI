from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name="assignment-2-CI",
    version="0.1.0",
    description="Continuous Integration assignment",
    author="Albin W Woxnerud, Riccardo Coco, Elias Bosæus Fröde and Dmitry Chirin",
    author_email="soffan.dd2480@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 2 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
