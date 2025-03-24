.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pyinstaller chatterblocker.py

	rm -rf __pycache__
	rm -rf .venv