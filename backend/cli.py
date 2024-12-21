import sys
import asyncio
import logging
from typing import Optional

from backend.services.article_generator import ArticleGenerator
from backend.schemas.article import ArticleRequest
from backend.utils.logger import setup_logging

async def generate_article(description: str, core_idea: Optional[str] = None) -> str:
    """
    异步生成文章
    
    Args:
        description: 文章描述
        core_idea: 核心主题（可选）
        
    Returns:
        str: 生成的文章文件路径
    """
    generator = ArticleGenerator()
    request = ArticleRequest(description=description, core_idea=core_idea)
    
    try:
        response = await generator.generate(request)
        return response.file_path
    except Exception as e:
        logger.error(f"生成文章时发生错误: {str(e)}")
        raise

def main():
    """命令行主函数"""
    # 设置日志
    global logger
    logger = setup_logging()
    
    # 检查参数
    if len(sys.argv) < 2:
        print("使用方法: python -m backend.cli <文章描述> [核心主题]")
        sys.exit(1)
    
    description = sys.argv[1]
    core_idea = sys.argv[2] if len(sys.argv) > 2 else None
    
    logger.info(f"开始生成文章，描述：{description}，核心主题：{core_idea}")
    
    try:
        filename = asyncio.run(generate_article(description, core_idea))
        logger.info(f"文章已生成并保存到：{filename}")
        print(f"文章已生成并保存到：{filename}")
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        print(f"发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 