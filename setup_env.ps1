Set-Location T:\OneDrive\Holger\OneDrive\Development\Python\islenska
# virtualenv venv391 -p D:\bin\Python\Python391\python.exe
# .\venv391\Scripts\activate.ps1
virtualenv venv392 -p D:\bin\Python\Python39\python.exe

.\venv392\Scripts\activate.ps1
python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
python -m ipykernel install --user --name=islenska