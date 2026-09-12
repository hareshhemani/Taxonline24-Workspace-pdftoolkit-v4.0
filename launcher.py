import os
import sys
import streamlit.web.cli as stcli

# --- WE MUST IMPORT THESE HERE SO THE .EXE KNOWS TO PACK THEM ---
import PyPDF2
import PIL
import pdf2image
import img2pdf
import pytesseract
import fitz
import tabula
import pandas
import openpyxl
import reportlab
import docx

if __name__ == "__main__":
    # Tell the .exe exactly where to find app.py hidden inside itself
    if getattr(sys, 'frozen', False):
        app_path = os.path.join(sys._MEIPASS, "app.py")
    else:
        app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
        
    # Launch Streamlit natively
    sys.argv = ["streamlit", "run", app_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())
