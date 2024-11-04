DIRECTORY="./Result"

if [ ! -d "$DIRECTORY" ]; then
  mkdir "$DIRECTORY"
fi

python ./DiffLenInf.py
python ./cmpResult.py