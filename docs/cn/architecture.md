# 架构

## 模块
- `vector2png/converters/ai.py`：AI 转换逻辑，方法决策，PyMuPDF 与 pdf2image 管线，背景处理。
- `vector2png/converters/dxf.py`：DXF 转换（ezdxf + PyMuPDF 后端），布局选择、尺寸与缩放。
- `vector2png/options.py`：`AIOptions` 与 `DXFOptions` 数据类。
- `vector2png/cli.py`：CLI 参数解析与转换器调用。
- `vector2png/utils.py`：路径、可选依赖导入等工具函数。

## AI 流程
1. 判断是否 PDF 基，确定渲染顺序。
2. 按顺序渲染：
   - PyMuPDF：渲染页为 pixmap；若非透明且指定背景色，用 Pillow 合成。
   - pdf2image：调用 Poppler；非透明且指定背景色同样用 Pillow 合成。
3. 若启用回退，首选失败时尝试次选。

## DXF 流程
1. 使用 ezdxf 解析。
2. 选择布局（默认 modelspace），构建渲染配置（背景、色彩策略、缩放、页面尺寸）。
3. 通过 ezdxf PyMuPDF 后端输出 PNG 字节。

## 扩展点
- 在现有接口旁新增转换器及其 options。
- 扩展 AI 的渲染方法与决策规则。
- 增加批处理或新格式（如 SVG/PDF），复用同样的选项模式。

## 设计考量
- 可选依赖分离，通过 `DependencyMissingError` 明确提示。
- 背景处理显式化，避免用户请求底色时静默白底。
- 数据类保持 API 易发现、易补全。 
- 管线基于 2D 页面渲染（PyMuPDF/Poppler + ezdxf 绘图），不具备 3D 光栅化或特效渲染能力。 
