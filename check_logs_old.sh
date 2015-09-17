if [ -z "${1}" ]; then
  re="*.log"
  find . -name "$re"
  for f in $(find . -name "$re"); do echo $f; grep -i iteration $f | tail -2; done
else
  for re in "$@"
  do
    for f in $(find . -name "$re"); do echo $f; grep -i iteration $f | tail -2; done
  done

fi
