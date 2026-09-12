# 💼 Taxonline24 Workspace - All-in-One PDF & Document Solution

A high-performance, secure, and intuitive desktop document management workspace built with **Python** and **Streamlit**. Specifically designed for financial professionals, tax practitioners, and document-heavy workflows to process, convert, manipulate, and secure PDF documents completely offline.

---

## 🌟 Key Features

### 🛠️ PDF Manipulation
* **🔗 Merge PDFs:** Combine multiple PDFs with custom page reordering and file sequencing.
* **✂️ Split PDF:** Extract specific pages or split documents by custom ranges.
* **🗜️ Deep Compress:** 
  * *Native PDFs:* Strip unneeded metadata and deflate code streams.
  * *Scanned PDFs:* Multi-level image downsampling and optimization (Normal, Aggressive, Extreme Black & White).
* **🔄 Rotate Pages:** Rotate 90°, 180°, or 270° permanently across all or selected pages.
* **📑 Organize Pages:** Rearrange, duplicate, or delete specific pages visually.
* **📐 Crop Margins:** Trim unwanted margins and borders using standard inch measurements.

### 🔄 Document Conversion
* **📘 PDF to Word (`.docx`):** High-fidelity document conversion retaining fonts, layouts, and OCR text from scanned pages.
* **📊 PDF to Excel (`.xlsx`):** Extract tabular data into spreadsheets with smart multi-page table consolidation.
* **🖼️ PDF to Image & 📄 Image to PDF:** Convert PDF pages into high-resolution JPG/PNG images or stitch photos into a unified PDF.
* **📝 PDF to Text:** Fast plaintext extraction for data ingestion or indexing.

### 🔒 Security & Advanced
* **🔑 Password Protect:** Encrypt sensitive financial documents with strong standard encryption.
* **🔓 Remove Protection:** Decrypt and unlock authorized PDF documents.
* **©️ Watermark:** Add custom diagonal text watermarks with opacity and angle controls.
* **✍️ Sign PDF:** Place digital signature stamps on documents.
* **⬛ Smart Redaction:** Permanently sanitize documents by redacting keywords or sensitive data with irreversible black boxes.
* **👁️ OCR Scanner:** Optical Character Recognition powered by Tesseract engine to extract text from scanned bills, receipts, and forms.

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have **Python 3.8+** installed on your system.

#### External Dependencies (Required for OCR and Image rendering):
* **Tesseract OCR:** 
  * Install to `C:\Program Files\Tesseract-OCR\tesseract.exe` (or keep a portable folder `Tesseract-OCR/` inside the project root).
* **Poppler for Windows:** 
  * Extract to `C:\poppler\Library\bin` (or keep a portable folder `poppler/` inside the project root).

---

### 2. Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/taxonline24-workspace.git
   cd taxonline24-workspace
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   ```

3. **Install required Python packages:**
   ```bash
   pip install streamlit PyPDF2 Pillow pdf2image img2pdf pytesseract PyMuPDF pdf2docx python-docx tabula-py pandas openpyxl reportlab
   ```

---

## 💻 How to Run

### Option A: Using Streamlit Command
```bash
streamlit run app.py
```

### Option B: Using Windows Batch Script
Simply double-click **`Run.bat`** to start the local server and launch the workspace in your default web browser automatically.

---

## 📦 Building a Standalone Windows Executable (.exe)

This project includes built-in PyInstaller automation to compile the entire Streamlit application into a standalone Windows application:

```bash
python build.py
```
* The compiled executable and bundled assets will be generated inside the `dist/Taxonline24_Workspace` directory.

---

## 📂 Project Structure

```text
├── app.py                            # Main Streamlit application & processing engine
├── launcher.py                       # Executable entrypoint for PyInstaller
├── build.py                          # Build automation script
├── Taxonline24_Workspace.spec        # PyInstaller specification config
├── Run.bat                           # 1-click batch launcher for Windows
├── images.ico                        # Application branding icon
├── requirements_and_software.txt.txt # System and library requirements
└── README.md                         # Project documentation
```

---

## 👨‍💻 Developer & Credits

* **Developer:** Haresh Kumar Hemani
* **Website:** [www.taxonline24.in](https://www.taxonline24.in)
* **Email:** [contact@taxonline24.in](mailto:contact@taxonline24.in)

---

## 📄 License
Distributed under the MIT License.
