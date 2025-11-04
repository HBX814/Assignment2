@echo off
REM OPTIMIZED: Run all compositions with time tracking

echo ========================================
echo OPTIMIZED Batch Processing
echo ========================================

set start_time=%time%
set comp_count=0


set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp01_Al100_Fe00_Ni00...
cd Comp01_Al100_Fe00_Ni00
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp02_Al00_Fe100_Ni00...
cd Comp02_Al00_Fe100_Ni00
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp03_Al00_Fe00_Ni100...
cd Comp03_Al00_Fe00_Ni100
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp04_Al25_Fe75_Ni00...
cd Comp04_Al25_Fe75_Ni00
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp05_Al25_Fe00_Ni75...
cd Comp05_Al25_Fe00_Ni75
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp06_Al00_Fe25_Ni75...
cd Comp06_Al00_Fe25_Ni75
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp07_Al50_Fe50_Ni00...
cd Comp07_Al50_Fe50_Ni00
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp08_Al50_Fe00_Ni50...
cd Comp08_Al50_Fe00_Ni50
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp09_Al00_Fe50_Ni50...
cd Comp09_Al00_Fe50_Ni50
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp10_Al75_Fe25_Ni00...
cd Comp10_Al75_Fe25_Ni00
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp11_Al75_Fe00_Ni25...
cd Comp11_Al75_Fe00_Ni25
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp12_Al00_Fe75_Ni25...
cd Comp12_Al00_Fe75_Ni25
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp13_Al33_Fe34_Ni33...
cd Comp13_Al33_Fe34_Ni33
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp14_Al34_Fe33_Ni33...
cd Comp14_Al34_Fe33_Ni33
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp15_Al50_Fe25_Ni25...
cd Comp15_Al50_Fe25_Ni25
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp16_Al25_Fe50_Ni25...
cd Comp16_Al25_Fe50_Ni25
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp17_Al25_Fe25_Ni50...
cd Comp17_Al25_Fe25_Ni50
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp18_Al40_Fe40_Ni20...
cd Comp18_Al40_Fe40_Ni20
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp19_Al40_Fe20_Ni40...
cd Comp19_Al40_Fe20_Ni40
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp20_Al20_Fe40_Ni40...
cd Comp20_Al20_Fe40_Ni40
call run_all.bat
cd ..

set /a comp_count+=1
echo.
echo [Composition %comp_count%/21] Processing Comp21_Al60_Fe20_Ni20...
cd Comp21_Al60_Fe20_Ni20
call run_all.bat
cd ..

echo.
echo ========================================
echo ALL COMPOSITIONS COMPLETED!
echo Start: %start_time%
echo End: %time%
echo Total compositions: %comp_count%
echo ========================================
pause
