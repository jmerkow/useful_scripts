currtime=`date +%s`
date
echo  ---------------------------
if [ -z "${1}" ]; then
  re="*.log"
  find . -name "$re"
  for f in $(find . -name "$re"); do echo $f; tac $f | grep -m 2 -i "iteration [0-9]*,"; done
else
  for re in "$@"

  do
    for f in $(find . -name "$re"); do 
     filemtime=`stat -c %Y $1`
     diff=$(( (currtime - filemtime)))
     echo $f -- last  modified $diff seconds ago
     tac $f | grep -m 2 -i "iteration [0-9]*,"
     echo ""
  done
  done
fi
