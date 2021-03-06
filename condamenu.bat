@echo off

echo.
echo $ conda activate myenv  # activate myenv
echo $ conda deactivate      # deactivate current env
echo $ conda env list        # show env list
echo.
echo $ conda create --name myenv python3.6       # create python 3.6
echo $ conda create --name myenv python3.7       # create python 3.7
echo $ conda create --name myenv2 --clone myenv  # clone
echo $ conda remove --name myenv2 --all          # remove all
echo.
echo $ conda config --get channel_priority           # 
echo $ conda config --set channel_priority strict    # [recommended]
echo $ conda config --set channel_priority flexible  # 
echo.
echo $ conda config --get channels                   # 
echo $ conda config --add channels conda-forge       # [recommended]
echo $ conda config --remove channels conda-forge    # 
echo.
