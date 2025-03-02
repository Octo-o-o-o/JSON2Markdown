# Pre-compile regex patterns
CODE_BLOCK_PATTERN = re.compile(r'```.*?```', re.DOTALL)
HTML_TAG_PATTERN = re.compile(r'<\/?[a-z][^>]*>')
CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x1F\x7F]')

def style_filter(text: str, filter_flag: bool = True) -> str:
    """
    Filter special characters while preserving code blocks.
    
    Args:
        text: Input text to process
        filter_flag: Whether to enable filtering of special characters
        
    Returns:
        Processed text with code blocks preserved
    """
    if not filter_flag:
        return text
        
    # Preserve code blocks
    code_blocks = CODE_BLOCK_PATTERN.findall(text)
    text_without_code = CODE_BLOCK_PATTERN.sub('CODE_BLOCK', text)
    
    # Apply filters
    text_without_code = HTML_TAG_PATTERN.sub('', text_without_code)
    text_without_code = CONTROL_CHAR_PATTERN.sub('', text_without_code)
    
    # Restore code blocks
    for code_block in code_blocks:
        text_without_code = text_without_code.replace('CODE_BLOCK', code_block, 1)
    
    return text_without_code