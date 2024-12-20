import os
import sys
import logging
import asyncio
from datetime import datetime
from src.article_generator import ArticleGenerator
from src.config import Config
from typing import Optional

def setup_logging():
    """设置日志配置"""
    os.makedirs('logs', exist_ok=True)
    config = Config()
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(f'logs/{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

async def generate_article(description: str, core_idea: Optional[str] = None) -> str:
    """异步生成文章"""
    generator = ArticleGenerator()
    
    # 并发生成写作方向和标题
    directions = await generator.generate_directions(description, core_idea)
    title = await generator.generate_title(directions)
    
    # 生成内容
    content = await generator.generate_content(directions, title)
    
    # 保存文章
    filename = generator.save_article(title, content, directions)
    return filename

def main():
    setup_logging()
    
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
        logging.error(f"程序执行出错: {str(e)}")
        print(f"发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 