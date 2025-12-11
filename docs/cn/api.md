# API 参考

## AIConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`：`.ai` 路径
  - `target`：`.png` 路径（默认同名）
  - `options`：`AIOptions`
  - 可能抛出：`ConversionError`、`DependencyMissingError`、`FileNotFoundError`
- `get_info(ai_path) -> dict`：返回存在性、大小、是否 PDF 基、页数、尺寸。

使用示例

```python
from vector2png import AIConverter, AIOptions

# 200 DPI，透明输出
AIConverter().convert(
    "examples/files/example.ai",
    "examples/generated/ai_transparent.png",
    AIOptions(dpi=200, transparent=True),
)

# 强制 PyMuPDF，禁止回退；若未安装 Pillow 且设置 background，会抛出依赖错误
AIConverter().convert(
    "examples/files/example.ai",
    "examples/generated/ai_pymupdf_only.png",
    AIOptions(prefer_method="pymupdf", fallback=False, background_color=(240, 240, 240)),
)

# 查询 AI 信息（是否 PDF-based、页数、尺寸）
info = AIConverter().get_info("examples/files/example.ai")
print(info)
```

## AIOptions
```python
AIOptions(
    dpi=300,
    transparent=False,
    background_color=None,  # (R, G, B) 元组
    prefer_method="auto",   # auto|pymupdf|pdf2image
    fallback=True,
    timeout=30,
)
```

说明：
- 透明优先：`transparent=True` 会忽略 `background_color`。
- `background_color` 仅在非透明时生效；PyMuPDF 与 pdf2image 均会合成（需 Pillow）。
- `prefer_method` 控制渲染顺序；`fallback=False` 时失败不尝试次选。

函数式 API 快速用法

```python
from vector2png import ai_to_png, AIOptions

# 默认流程（auto 优先级，300 DPI）
ai_to_png("examples/files/example.ai", "examples/generated/ai_default.png")

# 显式使用 pdf2image，失败不回退，适合已安装 Poppler 的环境
ai_to_png(
    "examples/files/example.ai",
    "examples/generated/ai_pdf2image_only.png",
    AIOptions(prefer_method="pdf2image", fallback=False, dpi=150),
)
```

## DXFConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`：`.dxf` 路径
  - `target`：`.png` 路径（默认同名）
  - `options`：`DXFOptions`
  - 可能抛出：`ConversionError`、`DependencyMissingError`、`FileNotFoundError`

使用示例

```python
from vector2png import DXFConverter, DXFOptions

# 模型空间单色渲染，并加粗线宽
DXFConverter().convert(
    "examples/files/example.dxf",
    "examples/generated/dxf_monochrome.png",
    DXFOptions(color_policy="monochrome", lineweight_scaling=1.5),
)

# 渲染指定 layout，限制在 300x300mm 内，保持比例
DXFConverter().convert(
    "examples/files/example.dxf",
    "examples/generated/dxf_layout.png",
    DXFOptions(layout_name="Model", max_width=300, max_height=300, background="white"),
)

# 仅转换特定 layout 的便捷方法
DXFConverter().convert_layout(
    "examples/files/example.dxf",
    layout_name="Layout1",
    target="examples/generated/dxf_layout_only.png",
)
```

## DXFOptions
```python
DXFOptions(
    dpi=300,
    page_width=0,
    page_height=0,
    margins=20,
    scale=1.0,
    max_width=None,
    max_height=None,
    background="white",     # white|black|default|off
    color_policy="color",   # color|black|white|monochrome
    lineweight_scaling=1.0,
    layout_name=None,
    pdsize=None,
    normalize_relative_size=False,
)
```

场景提示
- `layout_name` 未找到会抛出 `ConversionError`，可先查看 `doc.layouts.names()`。
- `page_width/page_height` 单位为毫米；`max_width/max_height` 用于限制页面并保持比例。
- `background` 与 `color_policy` 控制底色/线色组合，`lineweight_scaling` 可整体加粗/变细线宽。
- `pdsize`<=0 会被设为 1 以避免 ezdxf 相对点大小提示；`normalize_relative_size` 会把 MTEXT 相对字号 \\H...x 展开为绝对值。

函数式 API 快速用法

```python
from vector2png import dxf_to_png, DXFOptions

# 默认渲染
dxf_to_png("examples/files/example.dxf", "examples/generated/dxf_default.png")

# 渲染特定 layout，单色，A3 页面，20mm 边距
dxf_to_png(
    "examples/files/example.dxf",
    "examples/generated/dxf_a3_layout.png",
    DXFOptions(layout_name="Model", page_width=420, page_height=297, color_policy="monochrome", margins=20),
)
```

## 异常
- `ConversionError`：通用转换失败（空页面、输出为空、布局不存在/空布局、无效边界框、页面几何异常等）。CLI 仅输出单行提示，不再打印 Python traceback。
- `DependencyMissingError`：可选依赖缺失，消息包含安装提示。

错误处理示例

```python
import logging
from vector2png import ai_to_png, ConversionError, DependencyMissingError

logging.basicConfig(level=logging.INFO)

try:
    ai_to_png("examples/files/example.ai", "examples/generated/ai_error_demo.png")
except DependencyMissingError as exc:
    # 提示用户安装 pdf2image/Pillow/ezdxf 等
    print(f"缺少依赖: {exc}")
except ConversionError as exc:
    print(f"转换失败: {exc}")
```

## 日志
转换器本身轻量，可在应用中按需开启：
```python
import logging
logging.basicConfig(level=logging.INFO)
``` 
