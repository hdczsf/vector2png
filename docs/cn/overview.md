# vector2png 概览

`vector2png` 用精简、可测试的 Python 核心，将 Adobe Illustrator (AI) 与 DXF 文件转换为清晰的 PNG。AI 提供 PyMuPDF 与 pdf2image 双渲染路径，DXF 通过 ezdxf + PyMuPDF 后端渲染。

## 特性亮点
- 简洁 CLI 与 Python API，参数用数据类暴露，便于自动补全。
- AI 双渲染：默认 PyMuPDF，可切 pdf2image 或回退。
- 背景控制：透明优先，非透明时可指定底色。
- DXF 渲染支持布局选择、缩放与背景策略。
- MIT 许可，依赖按需拆分可选 extra。 

## 适用场景
- 2D 矢量内容（线条、形状、文字、渐变）到 PNG 预览。
- 在管线或 CI 中批量生成预览。
- 校验 DXF 布局或 AI 导出在指定 DPI 下的效果。
- 不支持 3D 对象或重度特效，请在上游展平/投影后再转换。 
