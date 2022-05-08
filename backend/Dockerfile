FROM python
RUN pip install --upgrade pip

WORKDIR /app
RUN mkdir data
COPY requirements.txt ./
COPY data ./data
RUN pip install -r requirements.txt --no-cache-dir
COPY . ./
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
RUN python manage.py collectstatic --no-input
# RUN python manage.py runscript load_ing_data