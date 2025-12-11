# 贡献指南

## 环境
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[full,dev]"
```

## 测试
```bash
PYTHONPATH=. pytest -q
```

## 编码约定
- 依赖尽量保持可选，使用 `optional_import` 并提供清晰提示。
- 保持数据类选项与默认值的一致性。
- 代码力求简洁可读，只有在逻辑不直观时才添加简短注释。
- 透明/背景优先级规则在各管线保持一致。

## 文档
- 行为或选项变更时同步更新 `README.md`/`README.cn.md` 及相关 `docs/*.md`。

## 发布
- 发布前在 `pyproject.toml` 中更新版本号。
- 确认可选 extra (`[ai]`, `[dxf]`, `[full]`) 定义正确。
- 发布前运行测试。 
