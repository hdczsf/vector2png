# CLI 使用指南

命令：`vector2png`

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
