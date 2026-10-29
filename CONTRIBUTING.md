# 项目维护与 GitHub 同步

## 每次修改的固定流程

1. 只完成一个清晰目标，例如补充文件读写、修正 HTTP 示例。
2. 修改手册与相关示例，更新 `CHANGELOG.md`。
3. 运行 `python tools/check_examples.py`。
4. 用 `git status --short`、`git diff` 检查改动，确认没有个人资料和密钥。
5. 暂存明确的文件并提交，推送到对应远程分支。

```powershell
git status -sb
git diff
git add README.md docs/开发基础手册.md CHANGELOG.md
git diff --staged
git commit -m "docs: 补充文件读写与异常处理"
git push
```

`git add` 的路径要按本次实际变更调整，新建文件在暂存前不会出现在普通 `git diff` 中。`git commit` 保存到本地，`git push` 才上传到 GitHub。

## 首次配置

先查看已有设置，不覆盖他人的远程配置：

```powershell
git remote -v
git branch --show-current
git config --get user.name
git config --get user.email
```

没有 Git 作者身份时，在本仓库设置自己的身份。下面的值是占位符，必须替换；邮箱可使用 GitHub 提供的隐私邮箱。

```powershell
git config user.name "你的提交显示名"
git config user.email "你的提交邮箱"
```

先在 GitHub 创建目标仓库。远程为空且尚无 `origin` 时，使用真实地址添加远程：

```powershell
git remote add origin https://github.com/你的用户名/你的仓库名.git
```

检查当前分支名后，用实际分支名进行首次推送。例如当前分支是 `master`：

```powershell
git push -u origin master
```

分支名不必和示例相同。若远程已有 README 或提交，先 `git fetch origin`、检查历史，再决定合并方式，不强行覆盖。

## 分支与多人协作

已同步主分支后，可以为较大修改建立功能分支：

```powershell
git switch -c codex/add-rag-notes
```

完成后推送该分支，在 GitHub 创建 Pull Request。小型个人笔记更新也可在已约定的当前分支直接维护。

有未提交改动时不要直接拉取。工作区干净且需要同步上游时：

```powershell
git pull --ff-only
```

如果提示分叉，先查看提交关系并协调，避免用强制推送解决。

## 认证与自动检查

HTTPS 推送通过系统的 Git 凭据管理器或 GitHub CLI 登录完成。不要把 Token 写进远程 URL、文档或脚本。若需提交邮箱，在 GitHub 个人设置中确认实际的隐私邮箱后再配置。

GitHub Actions 在推送和 Pull Request 时，对 Windows、Linux 上的 Python 3.13 运行示例检查。必须由 GitHub 实际执行成功后才能称为远程检查通过。

本项目不会自动定时提交。后续在此项目完成改动时，沿用“检查—提交—推送”流程。
