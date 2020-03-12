
basepath=$(cd `dirname $0`; pwd)

PATH=$basepath:$PATH
qc() {
    #setopt localoptions noautonamedirs
    # do quickcmd
    echo "---isshe---1---"
    $basepath/quickcmd ${@}
    ret=$?
    echo "---isshe---2---ret = $ret"
    if [ $ret -ne 0 ]; then
        echo "quickcmd error."
        echo "Try \`quickcmd --help\` for more information."
    fi

    # do cd cmd
    qc_cd_file="/tmp/.qc_cd_path"
    echo "---isshe---: qc_cd_file = $qc_cd_file"
    if [ -f $qc_cd_file ]; then
        cd_path=`cat "$qc_cd_file"`
        echo "cd \"$cd_path\""
        cd "$cd_path"
        #rm "$qc_cd_file"
    fi
}