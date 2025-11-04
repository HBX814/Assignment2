@echo off
REM Optimized job: FCC at 650K
REM Cores: 1 MPI × 8 OpenMP = 8 total

echo Running FCC at 650K (optimized settings)...

set OMP_NUM_THREADS=8
set OMP_PROC_BIND=spread
set OMP_PLACES=threads

cd /d "Comp11_Al75_Fe00_Ni25"

mpiexec -n 1 lmp -in in.FCC_650K.lammps > job_FCC_650K.out 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Job completed successfully!
) else (
    echo Job failed with error code %ERRORLEVEL%
)
