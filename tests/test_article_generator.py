import pytest
import os
from src.article_generator import ArticleGenerator
from src.config import Config

@pytest.fixture
def generator():
    return ArticleGenerator()

@pytest.mark.asyncio
async def test_generate_directions(generator):
    directions = await generator.generate_directions("测试文章", "测试主题")
    assert isinstance(directions, list)
    assert len(directions) >= 3
    assert len(directions) <= 5

@pytest.mark.asyncio
async def test_generate_title(generator):
    directions = ["方向1", "方向2", "方向3"]
    title = await generator.generate_title(directions)
    assert isinstance(title, str)
    assert len(title) > 0

@pytest.mark.asyncio
async def test_generate_content(generator):
    directions = ["方向1", "方向2", "方向3"]
    title = "测试标题"
    content = await generator.generate_content(directions, title)
    assert isinstance(content, str)
    assert len(content) >= Config.MIN_WORD_COUNT
    assert len(content) <= Config.MAX_WORD_COUNT

def test_save_article(generator):
    title = "测试标题"
    content = "测试内容"
    directions = ["方向1", "方向2"]
    filename = generator.save_article(title, content, directions)
    assert os.path.exists(filename)
    os.remove(filename)  # 清理测试文件 