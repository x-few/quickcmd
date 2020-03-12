
basepath=$(cd `dirname $0`; pwd)

echo "basepath = $basepath"


PATH=$basepath:$PATH
qc() {
    #setopt localoptions noautonamedirs
    # do quickcmd
    "$($basepath/quickcmd ${@})"
    ret=$?
    if [ $ret -ne 0 ];then
        echo "quickcmd error."
        echo "Try \`quickcmd --help\` for more information."
        exit $ret
    fi

    # do cd cmd
}