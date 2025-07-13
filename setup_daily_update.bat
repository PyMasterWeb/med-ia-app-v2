@echo off
echo Configurando atualização automática diária do cache de doenças...
echo.

REM Obter o caminho atual
set CURRENT_DIR=%~dp0
set PYTHON_PATH=py

REM Criar tarefa agendada para executar diariamente às 2:00 AM
schtasks /create /tn "Med-IA Cache Update" /tr "%PYTHON_PATH% %CURRENT_DIR%update_cache.py" /sc daily /st 02:00 /f

echo.
echo Tarefa agendada criada com sucesso!
echo O cache será atualizado diariamente às 2:00 AM
echo.
echo Para verificar a tarefa: schtasks /query /tn "Med-IA Cache Update"
echo Para remover a tarefa: schtasks /delete /tn "Med-IA Cache Update" /f
echo.
pause 