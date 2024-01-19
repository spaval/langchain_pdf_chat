setup:
	pip3 install -r config/requirements.txt

enable:
	source venv/bin/activate

disable:
	deactivate

run:
	streamlit run main.py