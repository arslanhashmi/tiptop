
TipTop music app in Django
=======
This project includes a complete music application made in Django to handle users albums and songs.
## Getting Started
 1. Clone this repo on your local machine.
1. Assuming you are having Python 3.7 already in your machine.
1. Setup environment:
    1. cd tiptip
    1. virtualenv -p python3.7 ~/.virtualenvs/tiptip
    1. source ~/.virtualenvs/tiptip/bin/activate
    1. pip install -r requirements.txt
1. Migrate:
    ```
    python manage.py migrate
1. Run app:
    ```
    python manage.py runserver 127.0.0.1:<PORT>
1. To clean environment following commands can be used:
    1. deactivate
    1. rm -rf ~/.virtualenvs/tiptip
    1. find . -name "*.pyc" -exec rm -f {} \;