Set WSHShell = CreateObject("WScript.Shell")
WSHShell.Run "cmd /c C:\Users\sahan\AppData\Local\Programs\Python\Python311\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000", 0, False
WScript.Quit