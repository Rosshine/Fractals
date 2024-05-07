1. Install python
https://www.python.org/downloads/release/python-3123/
After python installation, set path to Environment Variable:
path: C:\Python3123\python.exe;C:\Python3123\Scripts;
2. Setup python virtual Environment
Open cmd
python3 -m pip install virutalenv
virtualenv venv
3. Activate virtual environment
cd venv\\Scripts\activate
4. Install the packages using the command,
python3 -m pip install -r requirements.txt
5. Run the server using the command,
uvicorn views:app --reload --port 8090
6. Access the apis using,
http://localhost:8090/<endpointname>
7. Run the unit tests using,


8. Run the command to see the coverage,
coverage run -m unittest test_views.py
coverage report -m views.py



