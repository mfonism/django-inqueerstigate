FROM python:3.6-slim-stretch


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install libraries needed for compiling DLIB
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*


# Install DLIB
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS


# Install libraries needed for compiling boost
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    git \
    g++ \
    make \
    wget \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*


# Install boost
RUN cd /home && wget http://downloads.sourceforge.net/project/boost/boost/1.60.0/boost_1_60_0.tar.gz \
    && tar xfz boost_1_60_0.tar.gz \
    && rm boost_1_60_0.tar.gz \
    && cd boost_1_60_0 \
    && ./bootstrap.sh --prefix=/usr/local --with-libraries=python \
    && ./b2 install \
    && cd /home \
    && rm -rf boost_1_60_0


# Set work directory
WORKDIR /app


# Install project dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# Mount project
COPY . .


# Add and run as non-root user
RUN adduser -D mfonism
USER mfonism
