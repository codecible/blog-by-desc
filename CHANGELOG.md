# Changelog

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## Unreleased

### Changed
- 优化项目结构
  * 移动 requirements.txt 到 backend 目录
  * 删除未使用的 Dockerfile 文件
  * 删除空的 scripts 目录
  * 更新文档以反映最新的项目结构

## [1.0.1] - 2024-12-28
### Added
- 支持预览环境
  * docker-compose.pre.yml支持上线前的预览环境部署搭建
  * 优化预览环境资源配置,调整容器CPU和内存限制
  * 增加Node.js内存限制到3GB,确保大型项目构建不会出现内存问题
  * 优化后端服务配置,增加健康检查和重启策略
  * 完善日志管理,统一配置json-file驱动和日志轮转
  * 添加volume挂载配置,支持日志和输出文件持久化
  * 配置预览环境专用网络,实现容器间安全通信

### Fixed
- 修复前端构建错误
  * 添加terser依赖安装步骤
  * 优化npm配置，使用阿里云镜像源
  * 调整构建命令顺序
- 修复nginx权限问题
  * 移除nginx.conf中的user指令
  * 调整pid文件位置到/tmp/nginx目录
  * 优化容器内目录权限设置
  * 统一在Dockerfile中设置运行用户

## [1.0.1] - 2024-12-27
### Added
- 配置管理优化
  * 实现配置类的单例模式
  * 优化配置加载和验证逻辑
  * 添加详细的配置日志记录
- 多AI提供商支持
  * 支持Monica AI和智谱AI
  * 实现AI提供商的动态切换
  * 优化API客户端工厂模式
  * 统一的API调用接口

### Changed
- 重构配置管理机制
  * 使用单例模式确保配置一致性
  * 优化配置验证和错误处理
  * 改进配置加载流程
- 优化API客户端实现
  * 统一使用配置单例
  * 改进日志记录
  * 完善错误处理

## [1.0.0] - 2024-12-26
### Added
- 部署上云
- 新增阿里云专用 Dockerfile
  * 添加 `backend_aliyun.Dockerfile` 使用阿里云镜像源
  * 添加 `frontend_aliyun.Dockerfile` 使用阿里云 Node 镜像
  * 添加 `nginx_aliyun.Dockerfile` 使用阿里云优化版 Nginx
  * 添加 `docker-compose.aliyun.yml` 用于阿里云环境部署
- 优化阿里云部署配置
  * 使用阿里云镜像仓库加速构建
  * 配置 npm 和 pip 使用阿里云镜像源
  * 优化容器资源限制配置
  * 完善日志管理配置

### Changed
- 调整构建配置适配阿里云环境
  * 更新包管理器从 apt 到 yum
  * 优化用户创建命令适配阿里云基础镜像
  * 调整文件权限和目录结构
  * 优化健康检查配置

## [0.3.0] - 2024-12-24
### Added
- Docker部署优化
  * 添加前后端独立的 `.dockerignore` 文件
  * 优化 Docker 构建上下文
  * 实现非root用户运行容器
  * 使用docker-compose管理容器
- 部署至aliyun

### Changed
- 调整 Docker 相关配置
  * 更新 Python 基础镜像到 3.11
  * 优化构建流程和文件组织
  * 分离前后端构建上下文
  * 删除根目录冗余的 `.dockerignore` 文件

## [0.2.0] - 2024-12-22

### Added
- 完成前端页面开发
  * 实现文章生成表单页面
  * 实现文章预览页面
  * 添加文章内容复制功能
  * 添加文章下载为Markdown功能
  * 添加返回编辑功能
- 完善前后端交互
  * 实现文章生成API调用
  * 添加错误处理和提示
  * 优化数据传递方式
- 文章展示功能
  * 支持Markdown渲染
  * 优化代码块显示
  * 添加写作方向卡片展示
  * 优化排版和间距

### Changed
- 重构路由结构，简化页面跳转逻辑
- 优化组件通信方式，采用props传递数据
- 改进错误处理机制
- 优化页面加载状态管理

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
- 项目代码重构，将现有Python代码迁移到`backend`目录
- 将 `controllers` 目录重命名为 `routers`，更符合FastAPI最佳实践
- 优化 `schemas` 目录结构，增强数据验证
- 更新项目文档，完善目录结构说明
- 删除未实现的预览功能相关代码
- API 调用重试机制
- 日志��录系统

## [0.1.0] - 2024-12-20

### Added
- 项目初始化
- 基础项目结构搭建
- README.md 文档
- 配置文件支持
- 环境变量管理
- API 客户端封装
- 文章生成器核心类