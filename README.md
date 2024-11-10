# quickcmd

简化命令输入，再也不用记那么多命令啦。

## 安装

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/x-few/quickcmd/master/install.sh)"
```

## 添加快捷命令

在`~/.quickmd/commands`目录中添加`一个`或`多个`存储命令的文件。命令格式如下：

```ini
[快捷命令名称]         # 模糊搜索时用到

# 类型为 command 时
command = <命令>
workdir = <工作目录>    # 默认当前目录

# 类型为 godir 时
godir = <跳转目录>

# 类型为 tip 时
tip = <提示>          # 用于记录信息，需要时进行展示

# 类型为 chatgpt 时
api_key = <API-Key>
multi_line_question = <True/False>
```

### 示例：

```ini
# 跳转到用户根目录
[go-home]
godir = ~/

[git-pull]
command = git pull origin ${branch}
workdir = ~/.quickcmd

[Ask ChatGPT]
api_key = ChatGPT-API-KEY
```

## 使用

- `qc -h`: 显示帮助信息
- `qc -l`: 列出所有命令
- `qc`: 启动快捷命令选择器

## 功能

### 已完成

- [x] `~/`支持
- [x] 变量支持
- [x] 列出所有命令 `-l`
- [x] 增删改快捷命令
  - [x] 增：`-a`
  - [x] 删：`-d`
  - [x] 改：`-m`
- [x] `-v` 选项支持显示cmd目录和qc的目录
- [x] `-i`: 安装 quickcmd
- [x] `-u`: 卸载 quickcmd
- [x] `-p`: 更新 quickcmd

### 待办事项

- [ ] 自动化安装脚本
- [ ] 增加测试用例
- [ ] 完善 fzf 的检查：是否存在
- [ ] 支持频率排序
- [ ] 支持最近排序
- [ ] 支持频率+最近，权重排序
- [ ] 使用配置文件进行一些配置
