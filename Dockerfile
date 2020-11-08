FROM alpine

RUN apk add --no-cache uwsgi-python3 python3 py3-pip python3-dev
RUN apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev

RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install requests
RUN pip3 install bs4
#RUN pip3 install lxml

COPY flask_app /code

CMD cd code && uwsgi --ini uwsgi.ini