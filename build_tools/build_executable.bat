@echo off

rem Get the directory path of the batch file
set "batch_dir=%~dp0"

@echo on

pyinstaller "%batch_dir%\..\app\main.py" ^
	--name "PDF facturatie programma" ^
	--onedir ^
	--add-data="%batch_dir%\..\images\;images" ^
	--add-data="%batch_dir%\..\defaults\;defaults" ^
	--exclude-module PIL ^
	--clean -y -w