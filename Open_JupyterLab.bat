@echo off
echo Opening JupyterLab in current directory...
set "current_dir=%cd%"
call jupyter-lab "%current_dir%"
