
PATH=/home/isshe/Persional/coding-life/P-Projects/quickcmd:$PATH
qc() {
    setopt localoptions noautonamedirs
    local output="$(quickcmd ${@})"
    echo "---isshe---output = $output"
    if [[ -d "${output}" ]]; then
        if [ -t 1 ]; then  # if stdout is a terminal, use colors
                echo -e "\\033[31m${output}\\033[0m"
        else
                echo -e "${output}"
        fi
        cd "${output}"
    else
        echo "quickcmd: directory '${@}' not found"
        echo "\n${output}\n"
        echo "Try \`quickcmd --help\` for more information."
        false
    fi
}