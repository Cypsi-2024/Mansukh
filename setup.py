from setuptools import setup, find_packages

setup(
    name='Mansukh',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Flask',
        'transformers',
        'gradio',
        'langchain',
        'pinecone',
        'huggingface_hub',
        'python-dotenv',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'mansukh=src.app:main'
        ]
    },
    description='A mental health chatbot application',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/Mansukh',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)