# 快速开始

## 安装
建议在虚拟环境中使用：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install vector2png
```

可选 extra：
- AI 相关：`pip install "vector2png[ai]"`（安装 `pdf2image`、`Pillow`）。
- DXF 相关：`pip install "vector2png[dxf]"`。
- 全部：`pip install "vector2png[full]"`。

## CLI 最小示例
```bash
# AI → PNG（默认优先 PyMuPDF）
vector2png ai input.ai output.png

# 透明背景
vector2png ai input.ai output.png --transparent

# 固定底色（非透明）
vector2png ai input.ai output.png --background 255,0,0

# DXF → PNG
vector2png dxf drawing.dxf output.png --scale 1.5 --background white
```

## Python 最小示例
```python
from vector2png import AIConverter, AIOptions

opts = AIOptions(dpi=300, transparent=False, background_color=(240, 240, 240))
AIConverter().convert("input.ai", "output.png", opts)
```

## 示例文件
`examples/files/` 下提供示例素材便于测试。 
