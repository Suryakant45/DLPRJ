# Deep Learning Project - X-Ray Classification

## Setup Instructions

### Git Setup
```bash
git init
git remote add origin <repository-url>
git remote -v
git pull origin main
```

### Environment Setup

#### Using Conda (Recommended)
```bash
# Create a conda environment
conda create -p env python=3.13 -y

# Activate the environment
# On Windows CMD:
conda activate .\env
# On Windows PowerShell:
conda activate .\env
# On Git Bash or Linux/Mac:
conda activate ./env

# Install required packages
pip install -r requirements_dev.txt
```

#### Using venv (Alternative)
```bash
python -m venv env

# Activate the environment
# On Windows:
env\Scripts\activate
# On Linux/Mac:
source env/bin/activate

# Install required packages
pip install -r requirements_dev.txt
```

## Running the Project
```bash
python main.py
```



