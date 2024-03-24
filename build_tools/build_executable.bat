rem Get the directory path of the batch file
set "batch_dir=%~dp"
echo Directory of the batch file: %batch_dir%
exit /b
pyinstaller "%batch_dir%\main.py" --name "PDF facturatie programma" --onedir --add-data "%batch_dir%\..\images\":images/ --add-data "%batch_dir%\..\defaults\":defaults/ --exclude-module PIL --clean -y -w
