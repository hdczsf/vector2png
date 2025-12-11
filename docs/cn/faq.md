# FAQ

**问：透明与背景色如何同时处理？**  
答：透明优先。`transparent=True` 时输出 RGBA，忽略 `background_color`；非透明时才会合成背景色（需 Pillow）。

**问：PyMuPDF 会应用 `background_color` 吗？**  
答：会，在 `transparent=False` 且已安装 Pillow 的情况下。未安装 Pillow 会抛出依赖错误，避免静默白底。

**问：能渲染 3D 对象或复杂特效吗？**  
答：不能。当前管线基于 2D 页面渲染（PyMuPDF/Poppler），请在上游先展平或投影 3D/特效后再转换。

**问：AI 渲染器的选择逻辑？**  
答：`auto`：PDF 基 AI 先 PyMuPDF，否则先 pdf2image；`pymupdf`/`pdf2image` 强制顺序。`fallback=False` 不尝试次选。

**问：什么时候选择 pdf2image？**  
答：需要与 Poppler 渲染保持一致时（例如生产管线用 Poppler），或已有 Poppler 环境。否则 PyMuPDF 依赖更少、速度更快。

**问：可以批量转换吗？**  
答：可用 shell 循环或小脚本调用 `AIConverter`/`DXFConverter`。暂未提供内置批量命令。

**问：透明输出仍然是白色？**  
答：源文件可能包含白色形状；透明无法移除已绘制内容。

**问：DXF 需要 pdf2image 吗？**  
答：不需要。DXF 使用 ezdxf + PyMuPDF 后端；需安装 PyMuPDF 和 ezdxf。 
