@echo off
SET outfile="pylint_output.txt"
del %outfile%
touch %outfile%
for %%i in (*.py) do pylint %%i >> %outfile%
