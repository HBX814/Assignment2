@echo off
REM Optimized job: HCP at 200K
REM Cores: 1 MPI × 8 OpenMP = 8 total

echo Running HCP at 200K (optimized settings)...

set OMP_NUM_THREADS=8
set OMP_PROC_BIND=spread
set OMP_PLACES=threads

cd /d "Comp10_Al75_Fe25_Ni00"

mpiexec -n 1 lmp -in in.HCP_200K.lammps > job_HCP_200K.out 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Job completed successfully!
) else (
    echo Job failed with error code %ERRORLEVEL%
)
