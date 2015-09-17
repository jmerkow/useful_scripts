if [ -z "${1}" ]; then
  re="*.log"
  find . -name "$re"
  for f in $(find . -name "$re"); do echo $f; tac $f | grep -m 2 -i iteration; done
else
  for re in "$@"
  do
    for f in $(find . -name "$re"); do echo $f; tac $f | grep -m 2 -i iteration; done
  done

fi
