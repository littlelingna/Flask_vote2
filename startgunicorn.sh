nohup gunicorn -w 4 -b 0.0.0.0:8888 manager:app > nohup.log 2>&1 &

#  nohup python manager.py runserver > nohup.log 2>&1 &

