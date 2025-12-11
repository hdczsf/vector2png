# 依赖说明

## 必需
- Python >= 3.9
- PyMuPDF (`pymupdf`)：AI 基础渲染；DXF 通过 ezdxf 后端也依赖。

## 可选 extra
- AI (`vector2png[ai]`):
  - `pdf2image`：AI 备用渲染器（需系统安装 Poppler）。
  - `Pillow`：非透明时合成背景色（适用于 PyMuPDF 与 pdf2image）。
- DXF (`vector2png[dxf]`):
  - `ezdxf`：DXF 解析与渲染辅助。

## 系统说明
- Poppler：仅 pdf2image 需要。确保 `pdftoppm` 在 PATH 上（Linux 安装 `poppler-utils`，macOS `brew install poppler`，Windows 可用 OSGeo4W 等途径）。
- PyMuPDF wheel：覆盖常见平台，需匹配 Python 版本。
- Pillow：当设置 `background_color` 且非透明时需要。

## 安装示例
```bash
# 基础（仅 PyMuPDF）
pip install vector2png

# AI 栈
pip install "vector2png[ai]"

# DXF 栈
pip install "vector2png[dxf]"

# 全部
pip install "vector2png[full]"
```

## 缺依赖行为
- 缺失可选依赖会抛出 `DependencyMissingError` 并给出安装提示。
- PyMuPDF + `background_color` 未安装 Pillow：会报错以避免静默白底。 
