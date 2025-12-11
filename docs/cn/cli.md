# CLI 使用指南

命令：`vector2png`

## 快速示例

AI 转换

```bash
# 200 DPI 基础预览
vector2png ai examples/files/example.ai examples/generated/ai_basic.png --dpi 200

# 透明导出（带 alpha 通道），忽略背景色
vector2png ai examples/files/example.ai examples/generated/ai_transparent.png --transparent

# 合成浅灰底色（pdf2image 或 PyMuPDF 透明输出路径需要 Pillow）
vector2png ai examples/files/example.ai examples/generated/ai_background.png --background 240,240,240

# 只用 PyMuPDF，失败不回退 pdf2image
vector2png ai examples/files/example.ai examples/generated/ai_pymupdf_only.png --prefer pymupdf --no-fallback
```

DXF 转换

```bash
# 默认模型空间，白底单色
vector2png dxf examples/files/example.dxf examples/generated/dxf_basic.png --color monochrome --background white

# 渲染指定 layout，设置缩放与 A3 页面（单位 mm）
vector2png dxf examples/files/example.dxf examples/generated/dxf_layout.png --layout Model --scale 0.8 --page-width 420 --page-height 297

# 限制在 300x300mm 盒子内并整体加粗线宽
vector2png dxf examples/files/example.dxf examples/generated/dxf_fit.png --max-width 300 --max-height 300 --lineweight 1.5

# 归一 MTEXT 相对字号并显式设置点大小，避免 ezdxf 提示
vector2png dxf examples/files/example.dxf examples/generated/dxf_textsize.png --normalize-relative-size --pdsize 2.5
```

> 说明：偏好 pdf2image 时需要 pdf2image+Poppler（合成背景需 Pillow）；DXF 必须安装 ezdxf。`--layout` 请填写实际存在的布局名称（示例文件只有 `Model`）。若布局没有可绘制实体，会提示空边界框，请切换到包含图元的布局。

## AI 子命令
```
vector2png ai <source.ai> [target.png]
  --dpi <int>            渲染 DPI（默认 300）
  --transparent          输出带透明通道的 RGBA PNG
  --background R,G,B     固定底色，仅在非透明时生效
  --prefer {auto,pymupdf,pdf2image}
                         首选渲染器（默认 auto）
  --no-fallback          失败时不再尝试次选渲染器
```

行为说明
- 透明优先：设置 `--transparent` 时会忽略 `--background`。
- `--background` 只在非透明时生效；PyMuPDF 与 pdf2image 路径都会合成底色（需要 Pillow）。
- `--prefer auto`：AI 为 PDF 基时先尝试 PyMuPDF，否则先尝试 pdf2image。
- 若 `--prefer pymupdf` 且设置了 `--background` 但未安装 Pillow，会抛出依赖错误。
- CLI 仅输出单行错误提示（不打印 traceback）；空/无效布局会给出明确的 `ConversionError`。

## DXF 子命令
```
vector2png dxf <source.dxf> [target.png]
  --dpi <int>            渲染 DPI（默认 300）
  --background {white,black,default,off}
  --color {color,black,white,monochrome}
  --scale <float>        缩放比例（默认 1.0）
  --layout <name>        布局名称（默认 modelspace）
  --page-width <float>   页面宽度（mm）
  --page-height <float>  页面高度（mm）
  --margins <float>      边距（mm，四边一致）
  --lineweight <float>   线宽缩放因子
  --max-width <float>    最大宽度（mm）
  --max-height <float>   最大高度（mm）
  --pdsize <float>       POINT 实体尺寸（<=0 会设为 1 避免 ezdxf 相对尺寸提示）
  --normalize-relative-size
                         归一 MTEXT 相对高度，避免尺寸异常
```

退出码
- 成功：`0`
- 转换/依赖错误：`1`（错误输出到 stderr） 
