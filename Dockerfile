FROM alpine:latest

RUN apk add --update --no-cache python3 && \
    find / -type d -name __pycache__ -exec rm -r {} +   && \
    rm -r /usr/lib/python*/ensurepip                    && \
    rm -r /usr/lib/python*/lib2to3                      && \
    rm -r /usr/lib/python*/turtledemo                   && \
    rm /usr/lib/python*/turtle.py                       && \
    rm /usr/lib/python*/webbrowser.py                   && \
    rm /usr/lib/python*/doctest.py                      && \
    rm /usr/lib/python*/pydoc.py                        && \
    rm -rf /root/.cache /var/cache /usr/share/terminfo

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade requests

VOLUME /proc:/host-proc

ADD main.py main.py
ADD stats.py stats.py
ADD device.py device.py
CMD ["python3", "main.py"]
