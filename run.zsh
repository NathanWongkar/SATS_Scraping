#! /bin/zsh

if [[ $(date +%u) -gt 5 ]]; then
    python3 ./Weekend.py 
    exit
fi

python3 ./Weekday.py
