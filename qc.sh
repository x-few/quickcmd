
basepath=$(cd `dirname $0`; pwd)

PATH=$basepath:$PATH

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
    $basepath/quickcmd ${@}
    ret=$?
    if [ $ret -ne 0 ]; then
        qc_echo "quickcmd error. Try \`quickcmd --help\` for more information."
        return $ret
    fi

    # do cd cmd
    qc_cd_file="/tmp/.qc_cd_path"
    if [ -f $qc_cd_file ]; then
        cd_path=`cat $qc_cd_file`

        qc_echo "cd $cd_path"
        cd $cd_path
        rm $qc_cd_file
    fi
}