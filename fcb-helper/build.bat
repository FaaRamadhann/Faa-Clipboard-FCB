@echo off
rem Build fcb-helper.apk tanpa Android Studio (javac + d8 + aapt + apksigner).
rem Jalankan dari folder fcb-helper:  build.bat
setlocal
set BT=C:\AndroidSDK\build-tools\35.0.0
set PLAT=C:\AndroidSDK\platforms\android-34\android.jar
set JAVAC="C:\Program Files\Java\jdk-21.0.10\bin\javac.exe"
set KEYTOOL="C:\Program Files\Java\jdk-21.0.10\bin\keytool.exe"
if not exist build mkdir build
if not exist build\obj mkdir build\obj
if not exist build\dex mkdir build\dex

echo [1/6] javac...
%JAVAC% --release 8 -classpath "%PLAT%" -d build\obj src\com\faa\fcbclip\*.java
if errorlevel 1 exit /b 1

echo [2/6] d8...
call "%BT%\d8.bat" --min-api 24 --lib "%PLAT%" --output build\dex build\obj\com\faa\fcbclip\*.class
if errorlevel 1 exit /b 1

echo [3/6] aapt package...
"%BT%\aapt.exe" package -f -M AndroidManifest.xml -I "%PLAT%" -F build\unsigned.apk
if errorlevel 1 exit /b 1
cd build\dex
"%BT%\aapt.exe" add ..\unsigned.apk classes.dex
if errorlevel 1 exit /b 1
cd ..\..

echo [4/6] keystore (sekali saja)...
if not exist debug.keystore %KEYTOOL% -genkeypair -keystore debug.keystore -alias fcb -keyalg RSA -keysize 2048 -validity 10950 -storepass android -keypass android -dname "CN=FCB Helper"

echo [5/6] zipalign...
"%BT%\zipalign.exe" -f 4 build\unsigned.apk build\aligned.apk
if errorlevel 1 exit /b 1

echo [6/6] apksigner...
call "%BT%\apksigner.bat" sign --ks debug.keystore --ks-key-alias fcb --ks-pass pass:android --key-pass pass:android --out build\fcb-helper.apk build\aligned.apk
if errorlevel 1 exit /b 1

echo.
echo SELESAI: build\fcb-helper.apk
endlocal
