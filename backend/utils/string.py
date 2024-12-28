"""
字符串处理工具模块

这个模块包含了各种字符串处理的工具函数。
"""

def parse_bool(value: str) -> bool:
    """
    将字符串解析为布尔值

    Args:
        value: 要解析的字符串值，支持多种常见的布尔值表示：
              - True值: "true", "1", "yes", "on"
              - False值: "false", "0", "no", "off", ""

    Returns:
        bool: 解析后的布尔值

    Examples:
        >>> parse_bool("true")
        True
        >>> parse_bool("1")
        True
        >>> parse_bool("yes")
        True
        >>> parse_bool("false")
        False
        >>> parse_bool("0")
        False
        >>> parse_bool("")
        False
    """
    return str(value).lower() in ('true', '1', 'yes', 'on')
