DIRECTORY="./Result"

if [ ! -d "$DIRECTORY" ]; then
  mkdir "$DIRECTORY"
fi

python ./TestSyncGap.py ./SPT-at-13m/Strip0-File0.dat 0 > ./Result/MainMeter.txt
python ./TestSyncGap.py ./SPT-at-13m/Strip3-File0.dat 2 > ./Result/SubMeter.txt

python ./StatErr.py ./Result/MainMeter.txt ./Result/SubMeter.txt
