if not exist ".venv\Scripts\activate" (
    echo Creating virtual environment...
    python -m venv .venv
)

.venv\Scripts\activate && (
    python -m pip install -r requirements.txt
    python demo.py
)
