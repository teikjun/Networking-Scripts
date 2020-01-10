#!/bin/bash

genRandPorts() {
  gawk 'BEGIN{ srand(); print int(rand()*(65534-1025))+1025; print int(rand()*(65534-1025))+1025; print int(rand()*(65534-1025))+1025 }'
}

findPy3() {
  if [[ ! -z "$py3" ]]; then
    return
  fi
  py3="/usr/bin/python3"
  if [[ ! -x "$py3" ]]; then
    py3="$(which python3)"
    if [[ ! -x "$py3" ]]; then
      echo "Error: cannot find python3"
      py3=""
      return 1
    else
      echo "Warn: using python3 @ $py3"
    fi
  fi
}

run() {
  d0="$(dirname "$(readlink -f -- "$0")")"
  cd $d0
  pwd0="$(pwd)"
  pwd1=""
  inf=""
  ouf="$pwd0/msgs.txt"
  port=""
  
	export TERM=xterm
  tput smul; tput bold;
  echo "-- Test Case Amy(Python) --"
  tput sgr0;
    
  rm -f "msgs.txt" 2>/dev/null
  
  for p0 in $(genRandPorts); do
    port="$p0"
    
    cd ../bryan
    pwd1="$(pwd)"
    
    exec "$py3" "Bryan.py" "$port" &
    bpid="$!"
    
    cd ../amy
    #
    sleep 1
    if ! kill -0 $bpid 2>/dev/null; then
      port=""
      continue
    fi
    echo "Bryan running"
    exec "$py3" "Amy.py" "$port" &
    apid="$!"
    break
  done
  
  if [[ -z "$port" ]]; then
    tput rev;
    echo "Error: could not start up Bryan, perhaps due to conflicting port numbers?"
    kill -9 $bpid 2>/dev/null
    kill -9 $apid 2>/dev/null
    tput sgr0;
    return
  fi
  
  loops=0
  
  inf="$pwd1/docs.txt"
  iSize="$(wc -c "$inf" | awk '{print $1}')"
  while [[ $loops -lt 15 ]]; do
    if ! kill -0 $apid 2>/dev/null; then
      echo "Amy finished executing"
      break
    fi
    
    sleep 1
    loops=$(($loops + 1))
    if [[ $(($loops % 5)) -eq 0 ]]; then
      echo "$loops seconds elapsed"
    fi
  done

  kill -9 $apid 2>/dev/null
  kill -9 $bpid 2>/dev/null

  if [[ $added -ne 1 ]]; then
    diff "$ouf" "$inf"
    res=${PIPESTATUS[0]}
    tput rev;
    if [[ $res == "0" ]];
    then
      echo "Passed!"
    else
      echo "Failed:"
      oSize="$(wc -c "$ouf" | awk '{print $1}')"
      if [[ $oSize -lt $iSize ]];
      then
        echo "Output size smaller than input size"
        echo "Output size: $oSize"
        echo "Input size: $iSize"
      elif [[ $oSize -gt $iSize ]];
      then
        echo "Output size larger than input size"
        echo "Output size: $oSize"
        echo "Input size: $iSize"
      else
        echo "Output and input sizes match, but contents mismatch"
      fi
    fi
    tput sgr0;
  fi
  
  
}

findPy3
run
