# Changelog

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。


## Unreleased
### Added
- 生成的文章在网站上展示

## [0.1.2] - 2024-12-22

### Added
- 增强API文档功能
  * 添加详细的API请求/响应模型说明
  * 添加字段级别的验证规则和说明
  * 添加示例数据
  * 完善错误响应模型
- 优化数据模型结构
  * 添加基础响应模型（BaseResponse）
  * 添加统一的错误处理模型
  * 规范化API响应格式

### Changed
- - 项目代码重构，将现有Python代码迁移到`backend`目录
- 将 `controllers` 目录重命名为 `routers`，更符合FastAPI最佳实践
- 优化 `schemas` 目录结构，增强数据验证
- 更新项目文档，完善目录结构说明
- 删除未实现的预览功能相关代码
- API 调用重试机制
- 日志记录系统

## [0.1.0] - 2024-12-20

### Added
- 项目初始化
- 基础项目结构搭建
- README.md 文档
- 配置文件支持
- 环境变量管理
- API 客户端封装
- 文章生成器核心类