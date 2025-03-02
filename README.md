
# JSON 转 Markdown 工具

这是一个将JSON格式的对话记录转换为Markdown格式的工具，特别适合处理对话型数据的可视化展示。

尤其方便将auto-coder.chat的对话历史（chat_history.json，里面有很多符号，不便直接阅读）转换为 Markdown 格式，便于查阅和分享。

## 功能特性

1. 支持主对话记录和历史对话分组
2. 自动清理无效字符，保留Markdown结构
3. 支持代码块、标题、列表、表格等Markdown元素
4. 提供命令行界面，方便集成到工作流中

## 依赖安装

本工具需要以下Python库支持：

- Python 3.6+
- json (Python标准库)
- re (Python标准库)
- argparse (Python标准库)

## 历史消息对话组说明

工具支持处理历史对话分组，每个对话组会按照以下格式展示：

1. 每个对话组以`## 对话组 X`为标题，X从1开始编号
2. 组内每条消息以`### 角色名`为标题
3. 消息内容会进行自动清理，保留Markdown格式
4. 如果消息内容为空，会显示`*(空内容)*`作为占位符

## 使用说明

```bash
python json_to_markdown.py --json input.json --markdown output.md
```

参数说明：
- `--json`: 输入JSON文件路径（必需）
- `--markdown`: 输出Markdown文件路径（可选，不指定则打印到控制台）

## 示例

输入JSON结构示例：
```json
{
    "ask_conversation": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "您好！"}
    ],
    "conversation_history": [
        [
            {"role": "user", "content": "第一个问题"},
            {"role": "assistant", "content": "第一个回答"}
        ],
        [
            {"role": "user", "content": "第二个问题"},
            {"role": "assistant", "content": "第二个回答"}
        ]
    ]
}
```

输出Markdown示例：
```markdown
# 主对话记录

### User
你好

### Assistant
您好！

# 历史对话分组

## 对话组 1

### User
第一个问题

### Assistant
第一个回答

## 对话组 2

### User
第二个问题

### Assistant
第二个回答
```
