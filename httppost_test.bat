cls
@echo off
set /P URLREQUEST="URL����͂��Ă������� : "
curl -X POST %URLREQUEST% -d "device=7459E1&time=1603902940&data=12344"
@pause