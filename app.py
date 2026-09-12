import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image
import pdf2image
import img2pdf
import zipfile
import tempfile
import os
import sys
import math
import pytesseract
import fitz  # PyMuPDF
import re    # For Smart Sorting

# --- PORTABLE EXTERNAL ENGINE CONFIGURATION ---
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

pytesseract.pytesseract.tesseract_cmd = os.path.join(base_dir, 'Tesseract-OCR', 'tesseract.exe')

poppler_path_1 = os.path.join(base_dir, 'poppler', 'Library', 'bin')
poppler_path_2 = os.path.join(base_dir, 'poppler', 'bin')
if os.path.exists(poppler_path_2):
    POPPLER_PATH = poppler_path_2
else:
    POPPLER_PATH = poppler_path_1

# --- PAGE CONFIG ---
st.set_page_config(page_title="Taxonline24 | Workspace", page_icon="💼", layout="wide")

# --- NATIVE ADAPTIVE CSS ---
st.markdown("""
    <style>
    footer {visibility: hidden;}
    
    /* BULLETPROOF: Permanently hide the Streamlit Deploy button! */
    .stDeployButton { display: none !important; }
    [data-testid="stAppDeployButton"] { display: none !important; }
    
    /* PERFECT SPACING: Closes the massive gap at the top while keeping it below the 3 dots */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem; }
    
    [data-testid="column"] .stButton > button {
        height: 100px; 
        width: 100%; 
        border-radius: 12px;
        font-size: 18px; 
        font-weight: 600; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="column"] .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        border-color: #3B82F6; 
    }

    /* Category Headers */
    .cat-header {
        font-size: 14px; 
        text-transform: uppercase;
        letter-spacing: 1.5px; 
        margin-top: 20px; 
        margin-bottom: 5px; 
        font-weight: 700;
        color: var(--text-color);
        opacity: 0.6; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if 'page' not in st.session_state: 
    st.session_state.page = "Dashboard"

def change_page(target): 
    st.session_state.page = target

# --- LEFT SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='font-weight: 800; margin-top: -20px; color: var(--text-color);'>💼 Taxonline24</h2>", unsafe_allow_html=True)
    st.button("🏠 Dashboard", on_click=change_page, args=("Dashboard",), use_container_width=True)
    
    st.markdown("<div class='cat-header'>🛠️ Manipulation</div>", unsafe_allow_html=True)
    st.button("🔗 Merge PDFs", on_click=change_page, args=("Merge",), use_container_width=True)
    st.button("✂️ Split PDF", on_click=change_page, args=("Split",), use_container_width=True)
    st.button("🗜️ Compress", on_click=change_page, args=("Compress",), use_container_width=True)
    st.button("🔄 Rotate Pages", on_click=change_page, args=("Rotate",), use_container_width=True)
    st.button("📑 Organize Pages", on_click=change_page, args=("Organize",), use_container_width=True)
    st.button("📐 Crop PDF", on_click=change_page, args=("Crop",), use_container_width=True)
    
    st.markdown("<div class='cat-header'>🔄 Conversion</div>", unsafe_allow_html=True)
    st.button("🖼️ PDF to Image", on_click=change_page, args=("PDF2Img",), use_container_width=True)
    st.button("📄 Image to PDF", on_click=change_page, args=("Img2PDF",), use_container_width=True)
    st.button("📝 PDF to Text", on_click=change_page, args=("PDF2Text",), use_container_width=True)
    st.button("📘 PDF to Word", on_click=change_page, args=("PDF2Word",), use_container_width=True)
    st.button("📊 PDF to Excel", on_click=change_page, args=("PDF2Excel",), use_container_width=True)
    
    st.markdown("<div class='cat-header'>🔒 Security & Advanced</div>", unsafe_allow_html=True)
    st.button("🔑 Protect", on_click=change_page, args=("Protect",), use_container_width=True)
    st.button("🔓 Unprotect", on_click=change_page, args=("Unprotect",), use_container_width=True)
    st.button("©️ Watermark", on_click=change_page, args=("Watermark",), use_container_width=True)
    st.button("✍️ Sign PDF", on_click=change_page, args=("Sign",), use_container_width=True)
    st.button("⬛ Redact", on_click=change_page, args=("Redact",), use_container_width=True)
    st.button("👁️ OCR Scanner", on_click=change_page, args=("OCR",), use_container_width=True)

# --- SLEEK GLOBAL HEADER WITH INTEGRATED CREDIT ---
head_col1, head_col2 = st.columns([3, 1])

with head_col1:
    st.markdown("""
    <div style='margin-top: 0px;'>
        <h2 style='font-weight: 800; margin-bottom: 5px; color: var(--text-color);'>Welcome to Taxonline24 Workspace</h2>
        <p style='margin-top: 0px; margin-bottom: 10px; opacity: 0.7; font-weight: 500; color: var(--text-color);'>Secure document handling for financial professionals.</p>
    </div>
    """, unsafe_allow_html=True)
    
with head_col2:
    st.markdown("""
    <div style='text-align: right; padding-right: 10px; margin-top: 15px;'>
        <p style='margin: 0; font-size: 13px; opacity: 0.8; color: var(--text-color);'>Developed by <span style='font-weight: bold;'>Haresh Kumar Hemani</span></p>
        <p style='margin: 0; font-size: 12px; margin-top: 4px;'>
            <a href="https://www.taxonline24.in" target="_blank" style="color: #3B82F6; text-decoration: none; font-weight: 600;">taxonline24.in</a> &nbsp;|&nbsp; 
            <a href="mailto:contact@taxonline24.in" style="color: #3B82F6; text-decoration: none; font-weight: 600;">contact@taxonline24.in</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 10px; margin-bottom: 15px; border-color: var(--text-color); opacity: 0.2;'>", unsafe_allow_html=True)

# --- MAIN VIEW ROUTING ---
active = st.session_state.page
if active == "Dashboard":
    categories = {
        "🛠️ Manipulation": [("Merge", "Merge"), ("Rotate", "Rotate"), ("Split", "Split"), ("Organize", "Organize"), ("Compress", "Compress"), ("Crop", "Crop")],
        "🔄 Conversion": [("PDF to Img", "PDF2Img"), ("PDF to Word", "PDF2Word"), ("Img to PDF", "Img2PDF"), ("PDF to Excel", "PDF2Excel"), ("PDF to Text", "PDF2Text")],
        "🔒 Security & Advanced": [("Protect", "Protect"), ("Sign", "Sign"), ("Unprotect", "Unprotect"), ("Redact", "Redact"), ("Watermark", "Watermark"), ("OCR", "OCR")]
    }
    for cat_name, tool_list in categories.items():
        st.markdown(f"<h4 style='margin-top: 0px; margin-bottom: 12px; opacity: 0.9; color: var(--text-color);'>{cat_name}</h4>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, (label, target) in enumerate(tool_list):
            cols[idx % 3].button(label, on_click=change_page, args=(target,), use_container_width=True)

else:
    if st.button("← Back to Home"): 
        change_page("Dashboard")
        st.rerun()

    if active == "Merge":
        st.markdown("### 🔗 Merge PDFs")
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("Merge", type="primary"):
            merger = PdfMerger()
            progress_bar = st.progress(0, text="Preparing to merge...")
            
            for i, f in enumerate(files): 
                merger.append(f)
                progress_bar.progress((i + 1) / len(files), text=f"Merging file {i+1} of {len(files)}...")
            
            progress_bar.empty()
            out = BytesIO()
            merger.write(out)
            st.success("✅ Files successfully merged!")
            st.download_button("📥 Download Merged PDF", out.getvalue(), "merged.pdf", type="primary")

    elif active == "Split":
        st.markdown("### ✂️ Split PDF")
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            reader = PdfReader(file)
            c1, c2 = st.columns(2)
            start = c1.number_input("Start Page", 1, len(reader.pages), 1)
            end = c2.number_input("End Page", 1, len(reader.pages), len(reader.pages))
            
            if st.button("Split", type="primary"):
                writer = PdfWriter()
                total_pages = end - start + 1
                progress_bar = st.progress(0, text="Extracting pages...")
                
                for count, i in enumerate(range(start-1, end)): 
                    writer.add_page(reader.pages[i])
                    progress_bar.progress((count + 1) / total_pages, text=f"Extracting page {count+1} of {total_pages}...")
                
                progress_bar.empty()
                out = BytesIO()
                writer.write(out)
                st.success("✅ Document successfully split!")
                st.download_button("📥 Download Split PDF", out.getvalue(), "split.pdf", type="primary")

    elif active == "Compress":
        st.markdown("### 🗜️ Deep Compress PDF")
        file = st.file_uploader("Upload PDF", type="pdf")
        
        is_scanned = st.checkbox("This is a Scanned PDF (Aggressively shrink embedded images)")
        
        if is_scanned:
            st.info("Since this is a scan, choose how aggressively you want to shrink it.")
            strength = st.select_slider(
                "Image Compression Strength", 
                options=["Light", "Medium", "Aggressive", "Extreme (Black & White)"],
                value="Aggressive"
            )
        
        if file and st.button("Compress Now", type="primary"):
            try:
                original_size_mb = len(file.getvalue()) / (1024 * 1024)
                out = BytesIO()
                
                if is_scanned:
                    with st.spinner("Initializing image compression engine..."):
                        if strength == "Light":
                            target_dpi, quality, mode = 150, 60, 'RGB'
                        elif strength == "Medium":
                            target_dpi, quality, mode = 100, 40, 'RGB'
                        elif strength == "Aggressive":
                            target_dpi, quality, mode = 72, 30, 'RGB'
                        else:  
                            target_dpi, quality, mode = 72, 30, 'L'
                            
                        images = pdf2image.convert_from_bytes(file.read(), dpi=target_dpi, poppler_path=POPPLER_PATH)
                        compressed_imgs = []
                        
                    progress_bar = st.progress(0, text="Shrinking images...")
                    for i, img in enumerate(images):
                        img_io = BytesIO()
                        img.convert(mode).save(img_io, format="JPEG", quality=quality, optimize=True)
                        compressed_imgs.append(img_io.getvalue())
                        progress_bar.progress((i + 1) / len(images), text=f"Compressing page {i+1} of {len(images)}...")
                    
                    progress_bar.empty()
                    out_bytes = img2pdf.convert(compressed_imgs)
                    out.write(out_bytes)
                        
                else:
                    with st.spinner("Applying deep native compression..."):
                        doc = fitz.open(stream=file.read(), filetype="pdf")
                        doc.save(out, garbage=4, deflate=True)
                
                new_size_mb = len(out.getvalue()) / (1024 * 1024)
                
                if new_size_mb < original_size_mb:
                    st.success(f"✅ Success! Reduced size from **{original_size_mb:.2f} MB** to **{new_size_mb:.2f} MB**.")
                else:
                    st.warning(f"⚠️ This PDF is highly resistant to compression. Size remains **{new_size_mb:.2f} MB**.")
                    if is_scanned and strength != "Extreme (Black & White)":
                        st.info("Try cranking the slider up to 'Extreme (Black & White)'!")
                        
                st.download_button("📥 Download Compressed PDF", out.getvalue(), "compressed.pdf", type="primary")
            except Exception as e:
                st.error(f"Error compressing document: {e}")

    elif active == "Rotate":
        st.markdown("### 🔄 Rotate PDF")
        file = st.file_uploader("Upload PDF", type="pdf")
        angle = st.selectbox("Angle", [90, 180, 270, 360])
        
        if file and st.button("Rotate", type="primary"):
            reader = PdfReader(file)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            progress_bar = st.progress(0, text="Rotating pages...")
            
            for i, page in enumerate(reader.pages): 
                page.rotate(angle)
                writer.add_page(page)
                progress_bar.progress((i + 1) / total_pages, text=f"Rotating page {i+1} of {total_pages}...")
            
            progress_bar.empty()
            out = BytesIO()
            writer.write(out)
            st.success("✅ Document successfully rotated!")
            st.download_button("📥 Download Rotated PDF", out.getvalue(), "rotated.pdf", type="primary")

    elif active == "Organize":
        st.markdown("### 📑 Organize Pages")
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            reader = PdfReader(file)
            order = st.text_input("Page Order (e.g. 1,3,2)", "1")
            if st.button("Reorder", type="primary"):
                writer = PdfWriter()
                try:
                    pages_to_extract = order.split(',')
                    total_pages = len(pages_to_extract)
                    progress_bar = st.progress(0, text="Reorganizing pages...")
                    
                    for i, p in enumerate(pages_to_extract): 
                        writer.add_page(reader.pages[int(p)-1])
                        progress_bar.progress((i + 1) / total_pages, text=f"Moving page {i+1} of {total_pages}...")
                    
                    progress_bar.empty()
                    out = BytesIO()
                    writer.write(out)
                    st.success("✅ Pages successfully reorganized!")
                    st.download_button("📥 Download Reordered PDF", out.getvalue(), "organized.pdf", type="primary")
                except: 
                    st.error("Check page numbers. Ensure you are using commas without spaces (e.g., 1,3,2).")

    elif active == "Crop":
        st.markdown("### 📐 Crop Margins")
        st.info("Enter the amount of space you want to cut off from each side in **Inches** (e.g., 0.5 for half an inch).")
        file = st.file_uploader("Upload PDF", type="pdf")
        
        c1, c2, c3, c4 = st.columns(4)
        l_inch = c1.number_input("Left (Inches)", 0.0, 10.0, 0.0, step=0.1)
        r_inch = c2.number_input("Right (Inches)", 0.0, 10.0, 0.0, step=0.1)
        t_inch = c3.number_input("Top (Inches)", 0.0, 10.0, 0.0, step=0.1)
        b_inch = c4.number_input("Bottom (Inches)", 0.0, 10.0, 0.0, step=0.1)
        
        if file and st.button("Crop Document", type="primary"):
            reader = PdfReader(file)
            writer = PdfWriter()
            
            l = l_inch * 72; r = r_inch * 72; t = t_inch * 72; b = b_inch * 72
            total_pages = len(reader.pages)
            progress_bar = st.progress(0, text="Cropping pages...")
            
            for i, page in enumerate(reader.pages):
                page.mediabox.lower_left = (page.mediabox.left + l, page.mediabox.bottom + b)
                page.mediabox.upper_right = (page.mediabox.right - r, page.mediabox.top - t)
                writer.add_page(page)
                progress_bar.progress((i + 1) / total_pages, text=f"Cropping page {i+1} of {total_pages}...")
            
            progress_bar.empty()
            out = BytesIO()
            writer.write(out)
            st.success("✅ Margins successfully cropped!")
            st.download_button("📥 Download Cropped PDF", out.getvalue(), "cropped.pdf", type="primary")

    elif active == "PDF2Img":
        st.markdown("### 🖼️ PDF to Image (Lightning Fast Engine)")
        file = st.file_uploader("Upload PDF", type="pdf")
        c1, c2 = st.columns(2)
        img_format = c1.selectbox("Output Format", ["JPEG", "PNG"])
        quality = c2.selectbox("Quality", ["Standard (Faster)", "High Resolution (Slower)"])
        
        if file and st.button("Convert to Images", type="primary"):
            try:
                doc = fitz.open(stream=file.read(), filetype="pdf")
                total_pages = len(doc)
                zoom = 2 if quality == "High Resolution (Slower)" else 1
                mat = fitz.Matrix(zoom, zoom)
                zip_buffer = BytesIO()
                progress_bar = st.progress(0, text="Starting conversion...")
                
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    for i, page in enumerate(doc):
                        pix = page.get_pixmap(matrix=mat)
                        img_byte_arr = pix.tobytes(img_format.lower())
                        zf.writestr(f"page_{i+1}.{img_format.lower()}", img_byte_arr)
                        progress_bar.progress((i + 1) / total_pages, text=f"Processing page {i+1} of {total_pages}...")
                
                progress_bar.empty()
                st.success(f"✅ Successfully converted {total_pages} pages!")
                st.download_button("📥 Download ZIP Folder", zip_buffer.getvalue(), f"images.zip", type="primary")
            except Exception as e: 
                st.error(f"Error during conversion: {e}")

    elif active == "Img2PDF":
        st.markdown("### 📄 Image to PDF")
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs:
            st.success(f"✅ Loaded {len(imgs)} images.")
            
            def natural_sort_key(file_obj):
                return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', file_obj.name)]
            
            imgs_sorted = sorted(imgs, key=natural_sort_key)
            img_names = [img.name for img in imgs_sorted]
            
            st.markdown("<p style='font-size: 14px; margin-bottom: 0px; opacity: 0.8; color: var(--text-color);'>Verify or adjust the merge order below.</p>", unsafe_allow_html=True)
            final_order_names = st.multiselect("Merge Order", options=img_names, default=img_names)
            
            if final_order_names and st.button("Create PDF", type="primary"):
                img_dict = {img.name: img for img in imgs}
                final_imgs = [img_dict[name].read() for name in final_order_names]
                with st.spinner("Compiling images into PDF..."):
                    pdf_bytes = img2pdf.convert(final_imgs)
                    
                st.success("✅ PDF successfully created!")
                st.download_button("📥 Download PDF", pdf_bytes, "converted.pdf", type="primary")

    elif active == "PDF2Text":
        st.markdown("### 📝 PDF to Text")
        file = st.file_uploader("Upload PDF", type="pdf")
        if file and st.button("Extract Text", type="primary"):
            try:
                doc = fitz.open(stream=file.read(), filetype="pdf")
                total_pages = len(doc)
                full_text = ""
                progress_bar = st.progress(0, text="Extracting text blocks...")
                
                for i, page in enumerate(doc): 
                    full_text += page.get_text("text") + "\n\n"
                    progress_bar.progress((i + 1) / total_pages, text=f"Reading page {i+1} of {total_pages}...")
                
                progress_bar.empty()
                st.success("✅ Text successfully extracted!")
                st.text_area("Extracted Text", full_text, height=400)
                st.download_button("📥 Download Text File", full_text.encode('utf-8'), "extracted_text.txt", type="primary")
            except Exception as e: 
                st.error(f"Error extracting text: {e}")

    elif active == "PDF2Word":
        st.markdown("### 📘 PDF to Word Document")
        file = st.file_uploader("Upload PDF", type="pdf")
        is_scanned = st.checkbox("This is a Scanned PDF (Uses OCR to extract text from images)")
        
        if file and st.button("Convert to Word", type="primary"):
            if not is_scanned:
                try:
                    from pdf2docx import Converter
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp: 
                        tmp.write(file.read())
                        p = tmp.name
                    d = p.replace(".pdf", ".docx")
                    
                    with st.spinner("Analyzing layout and converting formatting to Word (this may take a moment)..."):
                        cv = Converter(p)
                        cv.convert(d)
                        cv.close()
                        
                        with open(d, "rb") as f: 
                            st.success("✅ Successfully converted to Word!")
                            st.download_button("📥 Download Word Doc", f.read(), "converted.docx", type="primary")
                except ImportError: 
                    st.error("⚠️ Library missing. Please run: `pip install pdf2docx`")
            else:
                try:
                    import docx 
                    with st.spinner("Initializing OCR Scanner on images..."):
                        images = pdf2image.convert_from_bytes(file.read(), poppler_path=POPPLER_PATH)
                        doc = docx.Document()
                        doc.add_heading('Converted Scanned Document', 0)
                        
                    progress_bar = st.progress(0, text="Reading text...")
                    for i, img in enumerate(images):
                        extracted_text = pytesseract.image_to_string(img)
                        doc.add_paragraph(extracted_text)
                        if i < len(images) - 1: 
                            doc.add_page_break()
                        progress_bar.progress((i + 1) / len(images), text=f"Scanning page {i+1} of {len(images)}...")
                    
                    progress_bar.empty()
                    out = BytesIO()
                    doc.save(out)
                    st.success("✅ OCR Conversion complete!")
                    st.download_button("📥 Download Editable Word Doc", out.getvalue(), "scanned_converted.docx", type="primary")
                except ImportError: 
                    st.error("⚠️ Library missing. Please open your terminal and run: `pip install python-docx`")
                except Exception as e: 
                    st.error(f"Error during OCR conversion: {e}")

    elif active == "PDF2Excel":
        st.markdown("### 📊 PDF to Excel Spreadsheet")
        file = st.file_uploader("Upload PDF with Tables", type="pdf")
        c1, c2 = st.columns(2)
        extraction_method = c1.radio("Table Structure:", ["Gridlines (Has visible borders)", "Whitespace (No visible borders)"])
        sheet_layout = c2.radio("Excel Sheet Organization:", ["Smart Combine (Combine matching tables into 2-3 sheets)", "One Sheet per Table (Default)"])
        
        if file and st.button("Convert to Excel", type="primary"):
            try:
                import tabula
                import pandas as pd
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp: 
                    tmp.write(file.read())
                    pdf_path = tmp.name
                
                use_lattice = True if extraction_method == "Gridlines (Has visible borders)" else False
                
                with st.spinner("Scanning document for table structures..."):
                    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, lattice=use_lattice, stream=not use_lattice)
                    
                if not tables:
                    st.warning("⚠️ No tables found. Try switching the Table Structure option.")
                else:
                    output = BytesIO()
                    progress_bar = st.progress(0, text="Formatting Excel sheets...")
                    
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        if "Smart Combine" in sheet_layout:
                            grouped_tables = {}
                            for idx, table in enumerate(tables):
                                clean_table = table.dropna(how='all', axis=1).dropna(how='all', axis=0)
                                col_count = len(clean_table.columns)
                                if col_count not in grouped_tables: 
                                    grouped_tables[col_count] = []
                                grouped_tables[col_count].append(clean_table)
                                progress_bar.progress((idx + 1) / len(tables), text=f"Analyzing table {idx+1} of {len(tables)}...")
                            
                            sheet_counter = 1
                            for col_count, table_list in grouped_tables.items():
                                combined_df = pd.concat(table_list, ignore_index=True)
                                combined_df.to_excel(writer, sheet_name=f"Group_{sheet_counter}_({col_count}_Cols)", index=False)
                                sheet_counter += 1
                                
                            progress_bar.empty()
                            st.success(f"✅ Successfully combined {len(tables)} messy tables into {len(grouped_tables)} smart sheets!")
                        else:
                            for i, table in enumerate(tables):
                                clean_table = table.dropna(how='all', axis=1).dropna(how='all', axis=0)
                                clean_table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
                                progress_bar.progress((i + 1) / len(tables), text=f"Writing table {i+1} of {len(tables)} to sheet...")
                                
                            progress_bar.empty()
                            st.success(f"✅ Successfully built an Excel file with {len(tables)} sheets!")
                    
                    st.download_button("📥 Download Excel Workbook (.xlsx)", output.getvalue(), "extracted_tables.xlsx", type="primary", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except Exception as e: 
                st.error(f"Error extracting tables: {e}")

    elif active == "Protect":
        st.markdown("### 🔑 Protect PDF")
        file = st.file_uploader("Upload PDF", type="pdf")
        pw = st.text_input("Password", type="password")
        
        if file and pw and st.button("Lock", type="primary"):
            reader = PdfReader(file)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            progress_bar = st.progress(0, text="Encrypting pages...")
            
            for i, p in enumerate(reader.pages): 
                writer.add_page(p)
                progress_bar.progress((i + 1) / total_pages, text=f"Encrypting page {i+1} of {total_pages}...")
                
            progress_bar.empty()
            writer.encrypt(pw)
            out = BytesIO()
            writer.write(out)
            st.success("✅ Document successfully locked!")
            st.download_button("📥 Download Protected PDF", out.getvalue(), "locked.pdf", type="primary")

    elif active == "Unprotect":
        st.markdown("### 🔓 Unprotect PDF")
        file = st.file_uploader("Upload PDF", type="pdf")
        pw = st.text_input("Password", type="password")
        
        if file and pw and st.button("Unlock", type="primary"):
            try:
                reader = PdfReader(file)
                reader.decrypt(pw)
                writer = PdfWriter()
                total_pages = len(reader.pages)
                progress_bar = st.progress(0, text="Decrypting pages...")
                
                for i, p in enumerate(reader.pages): 
                    writer.add_page(p)
                    progress_bar.progress((i + 1) / total_pages, text=f"Decrypting page {i+1} of {total_pages}...")
                    
                progress_bar.empty()
                out = BytesIO()
                writer.write(out)
                st.success("✅ Document successfully unlocked!")
                st.download_button("📥 Download Unlocked PDF", out.getvalue(), "unlocked.pdf", type="primary")
            except Exception as e:
                st.error("Incorrect Password or Corrupted File.")

    elif active == "Watermark":
        st.markdown("### ©️ Add Text Watermark")
        file = st.file_uploader("Upload Document", type="pdf")
        wm_text = st.text_input("Enter Watermark Text (e.g., CONFIDENTIAL)", "CONFIDENTIAL")
        
        if file and wm_text and st.button("Apply Watermark", type="primary"):
            try:
                from reportlab.pdfgen import canvas
                from reportlab.lib.colors import Color
                
                reader = PdfReader(file)
                writer = PdfWriter()
                
                first_page = reader.pages[0]
                width = float(first_page.mediabox.width)
                height = float(first_page.mediabox.height)
                
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=(width, height))
                can.translate(width / 2, height / 2)
                can.rotate(45)
                can.setFont("Helvetica-Bold", 85)
                can.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.25)) 
                can.drawCentredString(0, 0, wm_text)
                can.save()
                
                packet.seek(0)
                wm_pdf = PdfReader(packet)
                wm_page = wm_pdf.pages[0]
                
                total_pages = len(reader.pages)
                progress_bar = st.progress(0, text="Applying watermark...")
                
                for i, page in enumerate(reader.pages):
                    page.merge_page(wm_page)
                    writer.add_page(page)
                    progress_bar.progress((i + 1) / total_pages, text=f"Stamping page {i+1} of {total_pages}...")
                    
                progress_bar.empty()
                out = BytesIO()
                writer.write(out)
                st.success("✅ Watermark applied successfully!")
                st.download_button("📥 Download Watermarked PDF", out.getvalue(), "watermarked.pdf", type="primary")
            except ImportError: 
                st.error("⚠️ Library missing. Please open your terminal and run: `pip install reportlab`")
            except Exception as e: 
                st.error(f"Error applying watermark: {e}")

    elif active == "Sign":
        st.markdown("### ✍️ E-Sign Documents")
        file = st.file_uploader("Upload PDF Document", type="pdf")
        sig = st.file_uploader("Upload Signature Image", type=["png","jpg"])
        
        if file and sig and st.button("Apply Signature to All Pages", type="primary"):
            try:
                doc = fitz.open(stream=file.read(), filetype="pdf")
                sig_bytes = sig.read()
                total_pages = len(doc)
                progress_bar = st.progress(0, text="Applying signatures...")
                
                for i, page in enumerate(doc):
                    page_width = page.rect.width
                    page_height = page.rect.height
                    
                    sig_width = 150
                    sig_height = 50
                    margin = 40
                    
                    x1 = page_width - margin
                    y1 = page_height - margin
                    x0 = x1 - sig_width
                    y0 = y1 - sig_height
                    
                    sig_rect = fitz.Rect(x0, y0, x1, y1)
                    page.insert_image(sig_rect, stream=sig_bytes, keep_proportion=True)
                    progress_bar.progress((i + 1) / total_pages, text=f"Signing page {i+1} of {total_pages}...")
                
                progress_bar.empty()
                out = BytesIO()
                doc.save(out)
                st.success("✅ Signature successfully applied to the bottom-right of every page!")
                st.download_button("📥 Download Signed PDF", out.getvalue(), "signed.pdf", type="primary")
            except Exception as e: 
                st.error(f"Error applying signature: {e}")

    elif active == "Redact":
        st.markdown("### ⬛ Smart Redact")
        st.info("💡 **UI Tip:** To redact numbers with commas (like 3,12,10,500), separate different items using a **Semicolon (;)** or put them on a **New Line**.")
        
        file = st.file_uploader("Upload PDF", type="pdf")
        target = st.text_area("Words or numbers to black out (e.g. PAN12345; 3,12,10,500)")
        
        if file and target and st.button("Redact", type="primary"):
            # FIX: We replaced the code that was destroying commas. 
            # Now it only splits by New Line (\n) or Semicolon (;)
            raw_target = target.replace('\n', ';') 
            items = [i.strip() for i in raw_target.split(';') if i.strip()]
            
            doc = fitz.open(stream=file.read(), filetype="pdf")
            total_pages = len(doc)
            progress_bar = st.progress(0, text="Scanning for sensitive text...")
            
            for i, page in enumerate(doc):
                for t in items:
                    for r in page.search_for(t): 
                        page.add_redact_annot(r, fill=(0,0,0))
                page.apply_redactions()
                progress_bar.progress((i + 1) / total_pages, text=f"Redacting page {i+1} of {total_pages}...")
                
            progress_bar.empty()
            out = BytesIO()
            doc.save(out)
            
            # Added a message to show exactly what was redacted
            st.success(f"✅ Document successfully redacted! Items hidden: {', '.join(items)}")
            st.download_button("📥 Download Redacted PDF", out.getvalue(), "redacted.pdf", type="primary")

    elif active == "OCR":
        st.markdown("### 👁️ OCR Scanner")
        file = st.file_uploader("Scanned PDF", type="pdf")
        if file and st.button("Extract Text", type="primary"):
            with st.spinner("Initializing scanner..."):
                images = pdf2image.convert_from_bytes(file.read(), poppler_path=POPPLER_PATH)
                
            full_txt = ""
            progress_bar = st.progress(0, text="Scanning text...")
            
            for i, img in enumerate(images):
                full_txt += pytesseract.image_to_string(img) + "\n\n"
                progress_bar.progress((i + 1) / len(images), text=f"Scanning page {i+1} of {len(images)}...")
                
            progress_bar.empty()
            st.success("✅ OCR Scan complete!")
            st.text_area("Result", full_txt, height=300)
