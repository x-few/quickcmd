#!/bin/sh

qc_script_path=$(cd `dirname "$0"`; pwd)
qc_python_script="$qc_script_path/quickcmd.py"

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
        if [ -x "$(which python 2> /dev/null)" ]; then
            python "$qc_python_script" "$@"
        elif [ -x "$(which python3 2> /dev/null)" ]; then
            python3 "$qc_python_script" "$@"
        elif [ -x "$(which python2 2> /dev/null)" ]; then
            python2 "$qc_python_script" "$@"
        elif [ -x "/usr/bin/python" ]; then
            /usr/bin/python "$qc_python_script" "$@"
        elif [ -x "/usr/bin/python3" ]; then
            /usr/bin/python3 "$qc_python_script" "$@"
        elif [ -x "/usr/bin/python2" ]; then
            /usr/bin/python2 "$qc_python_script" "$@"
        else
            qc_echo "Error: not found python"
            return 1
        fi
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
        cd_path=`cat $qc_cd_file`

        qc_echo "cd $cd_path"
        cd $cd_path
        rm $qc_cd_file
    fi
}