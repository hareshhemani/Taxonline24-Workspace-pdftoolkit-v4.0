import os
import streamlit

# 1. Automatically find the hidden Streamlit HTML files
streamlit_path = os.path.dirname(streamlit.__file__)

# 2. Assemble the ultimate build command (with forced library imports)
command = (
    f'python -m PyInstaller --noconfirm --onedir --console --icon="images.ico" '
    f'--hidden-import="pdf2docx" '
    f'--hidden-import="reportlab" '
    f'--hidden-import="docx" '
    f'--add-data "app.py;." '
    f'--add-data "{streamlit_path};streamlit/" '
    f'--copy-metadata streamlit '
    f'--name="Taxonline24_Workspace" "launcher.py"'
)

# 3. Run the compiler
print("Starting the build process... please wait!")
os.system(command)
