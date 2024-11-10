#!/bin/bash

set -e

if ! command -v fzf &> /dev/null; then
    echo "Installing fzf ..."
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install
else
    echo "fzf is already installed"
fi

if [[ ! -d "$HOME/.quickcmd" ]]; then
    echo "downloading quickcmd ..."
    git clone --depth 1 https://github.com/x-few/quickcmd.git "$HOME/.quickcmd"
else
    echo "quickcmd directory is already exists"
fi

# installing python requirements
if command -v pip &> /dev/null; then
    pip install -r "$HOME/.quickcmd/requirements.txt"
elif command -v pip3 &> /dev/null; then
    pip3 install -r "$HOME/.quickcmd/requirements.txt"
else
    echo "pip is not installed"
fi

# Check shell type and add source command to appropriate rc file
shell_type=$(basename "$SHELL")
rc_file=""

if [[ "$shell_type" == "zsh" ]]; then
    rc_file="$HOME/.zshrc"
elif [[ "$shell_type" == "bash" ]]; then
    rc_file="$HOME/.bashrc"
else
    echo "Unsupported shell type: $shell_type"
    exit 1
fi

if ! grep -q "source.*quickcmd.sh" "$rc_file" 2>/dev/null; then
    echo "Adding quickcmd source to $rc_file"
    echo "[[ -s \"\$HOME/.quickcmd/quickcmd.sh\" ]] && source \"\$HOME/.quickcmd/quickcmd.sh\"" >> "$rc_file"
else
    echo "quickcmd source already exists in $rc_file"
fi
