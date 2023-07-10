# A CLI launcher for the linux environment

# Initialize constants
fn_egg="pyshepherd.egg-info"

# Initialize flags
egg_found=false

# Search for the egg
for item in *;do
  if [ "$item" = $fn_egg ];then
    printf "Egg found at %s!\\n" "$item"
    egg_found=true
  fi
done

# Install the egg if needed
if ! "$egg_found";then
  printf "Egg not found, installing..\\n"
  pip install -e .
fi

# Verify the interpreter
interpreter="./env/bin/python3"
if ! [ -f "$interpreter" ];then
  printf "Interpreter not found, exit!\\n" && exit
fi
printf "Interpreter found!\\n"

# Verify the script
script="./src/main.py"
if ! [ -f "$script" ];then
  printf "Script not found, exit!\\n" && exit
fi
printf "Script found!\\n"

# Launch the script with the interpreter
printf "Launching python application!\\n"
"$interpreter" "$script"
