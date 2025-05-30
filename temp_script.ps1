Remove-Item -Path "C:\Windows\Temp\*" -Force -Recurse
Remove-Item -Path "C:\Users\username\AppData\Local\Temp\*" -Force -Recurse
Clear-EventLog -LogName *