@echo off
REM OPTIMIZED: Run all simulations with time tracking

echo ========================================
echo Starting OPTIMIZED simulations
echo Total jobs: 9 (3 structures × 3 temps)
echo ========================================
echo.

set start_time=%time%
set job_num=0


set /a job_num+=1
echo [%job_num%/9] Running FCC at 400K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.FCC_400K.lammps > lammps_FCC_400K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed FCC at 400K
) else (
    echo   [✗] FAILED FCC at 400K
)

set /a job_num+=1
echo [%job_num%/9] Running FCC at 200K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.FCC_200K.lammps > lammps_FCC_200K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed FCC at 200K
) else (
    echo   [✗] FAILED FCC at 200K
)

set /a job_num+=1
echo [%job_num%/9] Running FCC at 650K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.FCC_650K.lammps > lammps_FCC_650K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed FCC at 650K
) else (
    echo   [✗] FAILED FCC at 650K
)

set /a job_num+=1
echo [%job_num%/9] Running HCP at 400K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.HCP_400K.lammps > lammps_HCP_400K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed HCP at 400K
) else (
    echo   [✗] FAILED HCP at 400K
)

set /a job_num+=1
echo [%job_num%/9] Running HCP at 200K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.HCP_200K.lammps > lammps_HCP_200K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed HCP at 200K
) else (
    echo   [✗] FAILED HCP at 200K
)

set /a job_num+=1
echo [%job_num%/9] Running HCP at 650K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.HCP_650K.lammps > lammps_HCP_650K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed HCP at 650K
) else (
    echo   [✗] FAILED HCP at 650K
)

set /a job_num+=1
echo [%job_num%/9] Running DHCP at 400K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.DHCP_400K.lammps > lammps_DHCP_400K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed DHCP at 400K
) else (
    echo   [✗] FAILED DHCP at 400K
)

set /a job_num+=1
echo [%job_num%/9] Running DHCP at 200K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.DHCP_200K.lammps > lammps_DHCP_200K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed DHCP at 200K
) else (
    echo   [✗] FAILED DHCP at 200K
)

set /a job_num+=1
echo [%job_num%/9] Running DHCP at 650K...
set OMP_NUM_THREADS=8 && mpiexec -n 1 lmp -in in.DHCP_650K.lammps > lammps_DHCP_650K.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [✓] Completed DHCP at 650K
) else (
    echo   [✗] FAILED DHCP at 650K
)

echo.
echo ========================================
echo All simulations completed!
echo Start time: %start_time%
echo End time: %time%
echo ========================================
pause
