ARG PYTHON_VERSION=3.10

FROM python:$PYTHON_VERSION
LABEL author="Mirko Mälicke"
LABEL maintainer="Mirko Mälicke"

# build the structure
RUN mkdir -p /src/camels_serv
RUN mkdir -p /src/dev/ezgs
RUN mkdir -p /src/dev/input_dir
RUN mkdir -p /src/dev/output_dir

# copy the sources
COPY ./camels_serv /src/camels_serv

# copy packageing
COPY ./requirements.txt /src/requirements.txt
COPY ./setup.py /src/setup.py
COPY ./README.md /src/README.md

# build the package
RUN pip install --upgrade pip
RUN cd /src && pip install -e .

# create the entrypoint
WORKDIR /src/camels_serv
ENTRYPOINT ["python"]
CMD ["server.py"]