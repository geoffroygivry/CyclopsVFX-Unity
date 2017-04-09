title Cyclops

::set up environment variables
set DI_ROOT=/Dropbox
set CYC_ROOT=%DI_ROOT%/Cyclops
set CYC_HYDRA_PATH=%CYC_ROOT%/Hydra
set CYC_CORE_PATH=%CYC_ROOT%/Core/config
set CYC_NUKE_ENV=%CYC_ROOT%/Core/config/NukeEnv
set CYC_MAYA_ENV=%CYC_ROOT%/Core/config/MayaEnv
set CYC_RV_ENV=%CYC_ROOT%/Core/config/RVEnv
set CYC_MARI_ENV=%CYC_ROOT%/Core/config/MariEnv
set CYC_3DE_ENV=%CYC_ROOT%/Core/config/3DeEnv
set CYC_CLARISSE_ENV=%CYC_ROOT%/Core/config/ClarisseEnv
set CYC_POLYPHEMUS_PATH=%CYC_ROOT%/Apps/Polyphemus
set CYC_METEOR_PATH=%DI_ROOT%/02_webDev/Meteor/subView
set CYC_STEROPES_PATH=%CYC_ROOT%/Apps/Steropes
set CYC_ENGINE_NUKE=%CYC_ROOT%/Apps/Engines/Nuke
set CYC_ICON=%CYC_CORE_PATH%/icons

set PYTHONPATH=%PYTHONPATH%;%CYC_ROOT%;%CYC_HYDRA_PATH%;%CYC_STEROPES_PATH%

set NUKE_PATH=%CYC_NUKE_ENV%
set SHOW_PATH=%DI_ROOT%/jobs

:: creation of "Aliases"
doskey nuke=nuke8.0.exe $*
doskey show=set JOB=$*
doskey shot=set SHOT=$*
doskey task=set TASK=$*
doskey maya="C:\Program Files\Autodesk\Maya2015\bin\maya.exe" $*
doskey clarisse="C:\Users\Geoffroy\Documents\clarisse\clarisse.bat" $*
set SHOW=%JOB%

:: start /B in cmd is the same as the '&' in linux, initialising the Dailies submissions database
::start /B mongod.exe --dbpath C:\Dropbox\Hydra_Db && cd C:\ && cls
cd C:\Dropbox\02_webDev\Meteor\subView
start /B meteor run
cd C:\
cls
