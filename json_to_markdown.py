import json
import re

def clean_content(content):
    """清理无效字符并保留Markdown结构"""
    cleaned = []
    in_code_block = False
    
    for line in content.split('\n'):
        # 代码块保护
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            cleaned.append(line)
            continue
            
        if in_code_block:
            cleaned.append(line)
            continue
            
        # 只清理行首空白（保留行尾空白和Markdown结构）
        line = re.sub(r'^[ \t]+', '', line)
        
        # 保留所有非空行或Markdown元素
        if line.strip() or any(re.match(p, line) for p in [
            r'^#{1,6}\s+.*',    # 标题
            r'^```[\s\S]*?```', # 代码块
            r'^-\s+.*',         # 列表项
            r'^\|.*\|.*',       # 表格
            r'!\[.*?\]\(.*?\)', # 图片
            r'\[.*?\]\(.*?\)',  # 链接
            r'^>\s+.*',         # 引用块
            r'^\*\s+.*',        # 无序列表
            r'^\d+\.\s+.*',     # 有序列表
            r'^---+\s*$',       # 分割线
        ]):
            cleaned.append(line)
    
    # 合并连续空行（最多保留两个空行）
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(cleaned)).strip()

def process_conversation_group(group, group_id):
    """统一对话组处理逻辑（与主对话相同）"""
    output = [f"\n## 对话组 {group_id + 1}\n"]
    
    for index, msg in enumerate(group):
        role = msg.get("role", "").title()
        content = msg.get("content", "").strip()
        
        # 保持与主对话完全相同的标题格式
        role_header = f"### {role}" if index == 0 else f"\n### {role}"
        output.append(role_header + "\n")
        
        if content:
            processed = clean_content(content)
            output.append(processed + "\n")
        else:
            output.append("*(空内容)*\n")
    
    return "".join(output).strip()

def json_to_markdown(data):
    """统一处理逻辑的主函数"""
    output = []
    
    # 主对话处理（保持原有成功逻辑）
    if "ask_conversation" in data:
        main_output = ["# 主对话记录\n"]
        for msg in data["ask_conversation"]:
            role = msg.get("role", "").title()
            content = msg.get("content", "").strip()
            
            main_output.append(f"### {role}\n")
            main_output.append(f"{clean_content(content)}\n\n" if content else "*(空内容)*\n\n")
        output.append("".join(main_output).strip())
    
    # 历史对话处理（使用统一逻辑）
    if "conversation_history" in data and data["conversation_history"]:
        history_output = ["\n\n# 历史对话分组"]
        for group_id, group in enumerate(data["conversation_history"]):
            if group and isinstance(group, list):
                history_output.append(process_conversation_group(group, group_id))
        output.append("\n".join(history_output))
    
    # 最终格式清理
    final_md = "\n\n".join(output)
    return re.sub(r'\n{3,}', '\n\n', final_md).strip()

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='将JSON对话转换为Markdown格式')
    parser.add_argument('--json', required=True, help='输入的JSON文件路径')
    parser.add_argument('--markdown', help='输出的Markdown文件路径（可选）')
    args = parser.parse_args()

    try:
        with open(args.json, 'r', encoding='utf-8') as f:
            input_json = json.load(f)
            
        markdown_output = json_to_markdown(input_json)
        
        if args.markdown:
            with open(args.markdown, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
        else:
            print(markdown_output)
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)