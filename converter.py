def style_filter(text):
    # Preserve code blocks
    code_blocks = re.findall(r'```.*?```', text, re.DOTALL)
    text_without_code = re.sub(r'```.*?```', 'CODE_BLOCK', text, flags=re.DOTALL)
    
    patterns = [
        r'<\/?[a-z][^>]*>',  # HTML tags
        r'[\x00-\x1F\x7F]'   # Control characters
    ]
    
    for pattern in patterns:
        text_without_code = re.sub(pattern, '', text_without_code)
    
    # Restore code blocks
    for code_block in code_blocks:
        text_without_code = text_without_code.replace('CODE_BLOCK', code_block, 1)
    
    return text_without_code