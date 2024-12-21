import sys
import asyncio
import logging
from typing import Optional

from src.utils.logger import setup_logging
from src.generators.blog_generator import BlogGenerator

async def generate_article(description: str, core_idea: Optional[str] = None) -> str:
    """异步生成文章"""
    generator = BlogGenerator()
    
    # 并发生成写作方向和标题
    directions = await generator.generate_directions(description, core_idea)
    title = await generator.generate_title(directions)
    
    # 生成内容
    content = await generator.generate_content(directions, title)
    
    # 保存文章
    filename = generator.save_article(title, content, directions)
    return filename

def main():
    # 设置日志
    logger = setup_logging()
    
    # 检查参数
    if len(sys.argv) < 2:
        print("使用方法: python main.py <文章描述> [核心主题]")
        sys.exit(1)
    
    description = sys.argv[1]
    core_idea = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        filename = asyncio.run(generate_article(description, core_idea))
        print(f"文章已生成并保存到：{filename}")
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        print(f"发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 