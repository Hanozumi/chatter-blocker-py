all: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pyinstaller chatterblocker.py

clean:
	rm -rf __pycache__
	rm -rf .venv
	rm -rf build
	rm -rf dist

service: dist/chatterblocker/chatterblocker
	sudo install -v chatter-blocker-py.service /usr/lib/systemd/system/chatter-blocker-py.service
	sudo sed -i "s@<path/to/executable>@$(realpath dist/chatterblocker/chatterblocker)@g" /usr/lib/systemd/system/chatter-blocker-py.service
	sudo systemctl enable --now chatter-blocker-py.service

rebuild:
	clean all