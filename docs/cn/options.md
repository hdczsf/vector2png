# 参数详解

## AI 参数与组合
- `dpi`：控制渲染分辨率，常用 144–600。
- `transparent`：
  - 为 `True`：输出 RGBA，背景透明；忽略 `background_color`。
  - 为 `False`：输出不透明；未指定背景色时默认为白色。
- `background_color`：
  - 仅在 `transparent=False` 时生效。
  - PyMuPDF 与 pdf2image 均会合成该底色（需要 Pillow）。
  - PyMuPDF + 设置背景色但未安装 Pillow 会抛出依赖错误。
- `prefer_method`：
  - `auto`：PDF 基的 AI 先 PyMuPDF，否则先 pdf2image。
  - `pymupdf` / `pdf2image`：强制顺序；`fallback` 控制是否尝试次选。
- `fallback`：`False` 时第一选择失败后不再尝试。

常见用法
- 透明 Logo：`transparent=True`，`prefer_method=pymupdf`。
- 品牌底色：`transparent=False`，`background_color=(R,G,B)`。
- 已有 Poppler 环境：`prefer_method=pdf2image` 以匹配 Poppler 渲染。

## DXF 参数
- `dpi`：光栅化 DPI，越高输出越大。
- `background`：white/black/default/off，对应 ezdxf 背景策略。
- `color_policy`：color/black/white/monochrome。
- `scale`：几何缩放比例。
- `layout_name`：指定布局，默认 modelspace。
- `page_width` / `page_height`：页面尺寸（mm，0 为自动）。
- `margins`：边距（mm，四边相同）。
- `max_width` / `max_height`：限制页面大小。
- `pdsize`：POINT 尺寸；<=0 会设为 1，避免 ezdxf 相对尺寸提示。
- `normalize_relative_size`：归一 MTEXT 相对高度，避免尺寸意外。 
