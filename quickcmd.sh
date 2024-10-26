#!/bin/sh

qc_script_path=$(cd `dirname "$0"`; pwd)
qc_python_script="$qc_script_path/quickcmd.py"
qc_venv_path="$qc_script_path/.qcvenv"

if [ ! -e "$qc_python_script" ]; then
    qc_script_path=$(readlink "$0")
    # qc_script_path=$(cd `dirname "$0"`; pwd)
    qc_python_script="$qc_script_path/quickcmd.py"
fi

qc_echo()
{
    msg=$1
    if [ -t 1 ]; then
        echo -e "\033[35m${msg}\033[0m"
    else
        echo ${msg}
    fi
}

qc()
{
    #setopt localoptions noautonamedirs
    # do quickcmd
    if [ -e "$qc_python_script" ]; then
        # Check if virtual environment exists, if not create it
        if [ ! -d "$qc_venv_path" ]; then
            qc_echo "Creating virtual environment..."
            python3 -m venv "$qc_venv_path"

            # Activate virtual environment
            source "$qc_venv_path/bin/activate"

            # Install or upgrade pip
            qc_echo "Upgrading pip..."
            pip install --upgrade pip

            # Install dependencies
            qc_echo "Checking and installing dependencies..."
            pip install -r "$qc_script_path/requirements.txt"
        else
            # Activate virtual environment
            source "$qc_venv_path/bin/activate"
        fi

        # Execute Python script in virtual environment
        python "$qc_python_script" "$@"

        # Deactivate virtual environment
        deactivate
    else
        qc_echo "Error: not found quickcmd.py"
        return 1
    fi

    ret=$?
    if [ $ret -ne 0 ]; then
        qc_echo "quickcmd error. Try \`quickcmd --help\` for more information."
        return $ret
    fi

    # do cd cmd
    qc_cd_file="$qc_script_path/.qc.cd.path"
    if [ -f $qc_cd_file ]; then
        cd_path=$(cat $qc_cd_file)

        # qc_echo "cd $cd_path"
        cd $cd_path
        rm -f $qc_cd_file
    fi
}
