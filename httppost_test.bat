cls
@echo off
set /P URLREQUEST="URL����͂��Ă������� : "
curl -X POST %URLREQUEST% -d "device=2&time=2019-01-01 12:00:00&data=ababababbababab"
@pause