# FAQ

**Q: How do transparency and background color interact?**  
A: Transparency wins. If `transparent=True`, the PNG is RGBA and `background_color` is ignored. If `transparent=False`, `background_color` fills the background (requires Pillow).

**Q: Does PyMuPDF honor `background_color`?**  
A: Yes, when `transparent=False` and Pillow is installed. Without Pillow, a dependency error is raised to avoid silent white backgrounds.

**Q: Can this render 3D objects or heavy visual effects?**  
A: No. The pipelines are 2D page renderers (PyMuPDF/Poppler). Flatten or project 3D/effects upstream before converting.

**Q: How does `prefer_method` work for AI?**  
A: `auto` picks PyMuPDF first for PDF-based AI, otherwise pdf2image first. `pymupdf` or `pdf2image` force the order. `fallback=False` stops after the first attempt.

**Q: When should I choose pdf2image?**  
A: When Poppler rendering matches your production pipeline or you need parity with Poppler-based tools. Otherwise PyMuPDF is faster and has fewer external dependencies.

**Q: Can I batch convert files?**  
A: Use shell loops or small Python scripts calling `AIConverter`/`DXFConverter`. There is no built-in batch command yet.

**Q: Why is my transparent output still white?**  
A: The source artwork may include a white shape; transparency cannot remove drawn content. Check the AI/PDF layers.

**Q: Do I need pdf2image for DXF?**  
A: No. DXF uses ezdxf with a PyMuPDF backend; ensure PyMuPDF and ezdxf are installed. 
