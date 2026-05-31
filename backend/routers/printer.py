from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import pygments
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from weasyprint import HTML, CSS

router = APIRouter(prefix="/api/printer", tags=["Printer"])

class PrintRequest(BaseModel):
    team_name: str
    machine_ip: str
    filename: str
    code: str

@router.post("/generate")
async def generate_pdf(req: PrintRequest):
    """
    将代码渲染为带有高亮的 PDF，供物理打印使用
    """
    try:
        lexer = get_lexer_for_filename(req.filename)
    except:
        from pygments.lexers import guess_lexer
        try:
            lexer = guess_lexer(req.code)
        except:
            from pygments.lexers import get_lexer_by_name
            lexer = get_lexer_by_name("text")
            
    formatter = HtmlFormatter(style='colorful', linenos=True, cssclass="source")
    highlighted_code = pygments.highlight(req.code, lexer, formatter)
    css_content = formatter.get_style_defs('.source')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @top-center {{
                    content: "{req.team_name} - {req.machine_ip} - {req.filename}";
                    font-size: 10pt;
                    font-family: monospace;
                    border-bottom: 1px solid #ccc;
                }}
                @bottom-right {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                }}
            }}
            body {{
                font-family: monospace;
                font-size: 11pt;
            }}
            .source {{
                background: #f8f8f8;
            }}
            {css_content}
        </style>
    </head>
    <body>
        {highlighted_code}
    </body>
    </html>
    """
    
    pdf_bytes = HTML(string=html_content).write_pdf()
    
    # 真实场景中这里可能还会调用 os.system("lp /tmp/xxx.pdf") 推送到打印机
    
    return Response(content=pdf_bytes, media_type="application/pdf")
