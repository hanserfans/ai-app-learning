# AI 应用开发学习

面向零基础学习者，以《深入理解 AI Agent：设计原理与工程实践》为主线，通过小实验逐步开发个人知识库学习助手。

公开仓库：[hanserfans/ai-app-learning](https://github.com/hanserfans/ai-app-learning)。

## 从这里开始

1. 阅读 [完整学习路线](AI应用学习路线图.md)：前 24 天建立基础，第 25–48 天完成应用工程主线，第 49–60 天为模型方向选修；后续每日任务见[进阶学习计划](docs/进阶学习计划.md)。
2. 使用 [Python 与开发基础速查手册](docs/开发基础手册.md)，边读边运行示例；循环部分包含 `enumerate`、关键字参数和解包的入门解释。
3. 完成一个小功能后，按 [项目维护约定](CONTRIBUTING.md)检查、提交和同步 GitHub。

手册按“知识点 → 业务场景 → 输入输出 → 常见失败”组织。重点场景包括知识库资料导入、问答引用编号、客服工单处理、模型接口调用和版本回滚。

## 运行示例

本阶段只使用 Python 标准库，无第三方依赖。示例以 Python 3.13 为基准。请在项目根目录运行：

```powershell
python examples/01_python_basics.py
python examples/02_functions.py
python examples/03_files_and_errors.py
python examples/04_http_demo.py
```

第三个示例会在 `data/learning_records.json` 保存演示学习记录；每次运行都会更新同一个演示文件。第四个示例临时启动本机 HTTP 服务，演示请求、JSON 与错误处理，不需要外网或 API Key。

一次检查全部示例：

```powershell
python tools/check_examples.py
```

检查脚本把文件演示写入临时目录，不修改个人学习数据。

## 目录

```text
AI应用学习路线图.md       完整路线与前 24 每日任务
docs/进阶学习计划.md      第 25–60 天业务项目与验收
docs/开发基础手册.md      概念、代码、命令与排错
examples/                可独立运行的基础示例
tools/check_examples.py  示例检查入口
CONTRIBUTING.md          GitHub 维护流程
CHANGELOG.md             内容更新记录
.github/workflows/       GitHub Actions 检查
```

## 维护方式

每次学习或功能修改后，更新对应说明，运行示例检查，查看差异，再提交并推送。当前是否已同步，以 `git status -sb` 与远程推送结果为准。仓库地址配置方式见维护约定。

## 参考

- [《深入理解 AI Agent》在线阅读](https://bojieli.github.io/ai-agent-book/)
- [原书配套仓库](https://github.com/bojieli/ai-agent-book)

本项目是学习笔记和独立练习，引用原书及官方文档时注明来源，不复制整本书。
