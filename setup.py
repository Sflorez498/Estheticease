from setuptools import setup, find_packages

setup(
    name="estheticease",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "pydantic>=1.8.0,<2.0.0",
        "uvicorn>=0.15.0,<0.16.0",
        "sqlalchemy>=1.4.0,<1.5.0",
        "passlib[bcrypt]>=1.7.4,<1.8.0",
        "python-jose[cryptography]>=3.3.0,<3.4.0",
        "python-multipart>=0.0.5,<0.0.6",
        "email-validator>=1.1.3,<1.2.0",
        "python-dotenv>=0.19.0,<0.20.0",
        "pymysql>=1.0.2,<1.1.0",
        "cryptography>=35.0.0,<36.0.0"
    ],
) 