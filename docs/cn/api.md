# API 参考

## AIConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`：`.ai` 路径
  - `target`：`.png` 路径（默认同名）
  - `options`：`AIOptions`
  - 可能抛出：`ConversionError`、`DependencyMissingError`、`FileNotFoundError`
- `get_info(ai_path) -> dict`：返回存在性、大小、是否 PDF 基、页数、尺寸。

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

## DXFConverter
- `convert(source, target=None, options=None) -> Path`
  - `source`：`.dxf` 路径
  - `target`：`.png` 路径（默认同名）
  - `options`：`DXFOptions`
  - 可能抛出：`ConversionError`、`DependencyMissingError`、`FileNotFoundError`

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

## 异常
- `ConversionError`：通用转换失败（空页面、输出为空、布局不存在等）。
- `DependencyMissingError`：可选依赖缺失，消息包含安装提示。

## 日志
转换器本身轻量，可在应用中按需开启：
```python
import logging
logging.basicConfig(level=logging.INFO)
``` 
