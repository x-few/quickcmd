# quickcmd
简化命令输入，再也不用记那么多命令拉。

# 安装
* 安装[fzf](https://github.com/junegunn/fzf)
* `git clone https://github.com/i-sout/quickcmd.git ~/.quickcmd`
* 在`~/.bashrc`或`~/.zshrc`或其他终端配置文件中，添加:
  * `[[ -s "~/.quickcmd/quickcmd.sh" ]] && source "~/.quickcmd/quickcmd.sh"`

# 添加快捷命令
* 在`~/.quickmd/commands`目录中添加`一个`或`多个`存储命令的文件。命令格式如下：
```shell
[快捷命令名称]  # 模糊搜索时用到
command=<命令>
workdir=<工作目录>  # 默认当前目录
godir=<跳转目录>    # 没有command时直接跳转
```
* 示例：
```
# 跳转到用户根目录
[go-home]
godir = ~/

[git-pull]
command = git pull origin ${branch}
workdir = ~/.quickcmd
```

# 使用
* `qc -h`
* `qc -l`
* `qc`

# TODO
* 自动化安装脚本
* 增删改快捷命令
  * 增：done
  * 删：done
  * 改：done
* `-h`选项支持显示cmd目录，和qc的目录。
    * 相关的一些目录，都列出来
* 完善 fzf 的检查：是否存在
* 支持频率排序
* 支持最近排序
* 支持频率+最近，权重排序


# Done
* `~/`支持
* 变量支持
