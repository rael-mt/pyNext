Portal 
======

Env
======

* Linux

````bash
    python -m venv env && source env/bin/activate && pip install -r backend/requirements.txt

    uvicorn app.main:app --reload

````

* Windows

````bash
    python -m venv venv && venv\Scripts\activate.bat && pip install -r backend/requirements.txt
````