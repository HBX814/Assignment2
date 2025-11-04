@echo off
REM Optimized job: DHCP at 400K
REM Cores: 1 MPI × 8 OpenMP = 8 total

echo Running DHCP at 400K (optimized settings)...

set OMP_NUM_THREADS=8
set OMP_PROC_BIND=spread
set OMP_PLACES=threads

cd /d "Comp12_Al00_Fe75_Ni25"

mpiexec -n 1 lmp -in in.DHCP_400K.lammps > job_DHCP_400K.out 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Job completed successfully!
) else (
    echo Job failed with error code %ERRORLEVEL%
)
