# vector2png

一套优雅的 Python 工具，帮助你将 Adobe Illustrator (`.ai`) 与 AutoCAD DXF (`.dxf`) 文件快速转换为高质量 PNG 预览图，兼顾直观 API 与易用 CLI 的使用体验。

## 特性亮点

- 直观的函数式 API（`vector2png.ai_to_png`、`vector2png.dxf_to_png`）与可配置的转换器类并存
- AI 转换支持 PyMuPDF + pdf2image 双方案，自动根据文件特性选择并可降级回退
- DXF 转换基于 `ezdxf` + `PyMuPdfBackend`，支持自定义布局、页面尺寸、颜色策略等
- 自带命令行工具，终端即可完成转换
- 可选安装 extra，按需拉取 pdf2image/Pillow/ezdxf，保持默认依赖精简

## 安装方式

```bash
pip install vector2png            # 安装核心 PyMuPDF 依赖
pip install vector2png[ai]        # 追加 pdf2image + Pillow，用于 AI 管线
pip install vector2png[dxf]       # 追加 ezdxf，用于 DXF 渲染
pip install vector2png[full]      # 一次性安装全部可选依赖
```

> pdf2image 依赖 Poppler。Windows 用户可通过 OSGeo4W 或 Chocolatey 安装 `pdftoppm.exe`，macOS 可执行 `brew install poppler`，Linux 请安装 `poppler-utils`。

### 许可证提示

PyMuPDF（MuPDF）默认使用 AGPLv3 协议。本项目在 AI 与 DXF 渲染上均依赖 PyMuPDF，因此任何基于本项目进行再分发或提供在线服务的用户，都必须遵守 AGPL 的开源义务，或向 Artifex 购买 MuPDF 商业授权。MIT 许可证仅覆盖本仓库代码，无法免除 PyMuPDF 带来的合规要求。

## 快速上手

### Python API

```python
from vector2png import ai_to_png, dxf_to_png, AIOptions, DXFOptions

ai_to_png("logo.ai", "logo.png", AIOptions(dpi=200, transparent=True))

options = DXFOptions(layout_name="ISO_A1", background="white", color_policy="monochrome")
dxf_to_png("floorplan.dxf", "floorplan.png", options)
```

### 命令行

```bash
vector2png ai source.ai output.png --dpi 200 --transparent
vector2png dxf drawing.dxf output.png --layout Layout1 --color monochrome
# DXF 相关辅助参数示例：
#   --pdsize 2.5                 # 显式设置点大小，避免 ezdxf 相对大小提示
#   --normalize-relative-size    # 将 MTEXT 中的 \\H...x 相对字号展开为绝对字号
```

运行 `vector2png --help` 查看全部参数与默认值。

## 示例代码

`examples/` 目录提供了简单脚本：

- `examples/ai_basic.py`：读取 `examples/files/example.ai` 并导出 PNG 预览。
- `examples/dxf_basic.py`：读取 `examples/files/example.dxf` 并导出 PNG 预览。

## 参数概览

| 转换器 | 核心参数 |
| ------ | -------- |
| AI | `dpi`、`transparent`、`background_color`、`prefer_method`、`fallback` |
| DXF | `dpi`、`background`、`color_policy`、`scale`、`layout_name`、`page_width`、`page_height`、`margins`、`lineweight_scaling`、`max_width`、`max_height`、`pdsize`、`normalize_relative_size` |

所有参数都封装在 `AIOptions`、`DXFOptions` 数据类中，可获得 IDE 补全与静态提示。

## 错误处理

转换过程中若出现异常会抛出 `ConversionError`（或更具体的 `DependencyMissingError`）。当缺少可选依赖时，异常消息会明确告知需要安装的 extra，CLI 也会输出同样的信息并以非零状态退出。

 

## 后续规划

- 扩展支持 SVG、PDF 等更多矢量格式
- 批量转换与并发控制
- 输出更丰富的诊断日志（页面尺寸、渲染耗时等）

## 致谢

- [PyMuPDF (MuPDF)](https://pymupdf.readthedocs.io/) 提供高质量的 PDF/AI 渲染能力。
- [pdf2image](https://github.com/Belval/pdf2image) 与 [Pillow](https://python-pillow.org/) 带来可选的 AI 渲染管线。
- [ezdxf](https://ezdxf.mozman.at/) 支持 DXF 解析与绘制。
- 对所有开源社区贡献者、测试与工具作者表示感谢。

欢迎提出建议或提交 PR，一起让 vector2png 更好用！
