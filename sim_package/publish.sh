# handle help message
Help()
{
   # Display Help
   echo "publish package to staging or prod "
   echo
   echo "Syntax: publish.sh ["prod"] [-h]"
   echo "positionals:"
   echo "1 -> positional arg that decides whether to push to production or staging(default)"
   echo "options:"
   echo "h -> Print this Help."
   echo
}

while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done

# install build package if not preinstalled, install twine for upload of package
python3 -m pip install build twine
# create distribution files
python3 -m build

if [ "$1" == "prod" ]; then 
  python3 -m twine upload dist/*
else
  python3 -m twine upload -r testpypi dist/*
fi
