from setuptools import setup, find_packages

setup(
    name="telegram-post",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "telethon>=1.28.5",
        "python-dotenv>=0.19.0",
        "psycopg2-binary>=2.9.5"
    ],
) 