FROM continuumio/miniconda3:4.10.3-alpine AS builder

ARG GITLAB_TOKEN

ENV GITLAB_TOKEN=$GITLAB_TOKEN

EXPOSE 8888

LABEL maintainer.name="Umesh Timalsina"\
      maintainer.url="https://isis.vanderbilt.edu"

ENV PATH /opt/conda/bin:$PATH

USER root

ADD . /symbench-athens-client

RUN apk --update add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/* && \
    apk add gfortran g++ automake make libtool autoconf sudo

WORKDIR /symbench-athens-client

RUN conda update conda -yq && \
  conda config --set always_yes yes --set changeps1 no && \
  . /opt/conda/etc/profile.d/conda.sh && \
  conda install -c conda-forge mamba && \
  mamba env create nomkl --file environment-docker.yml && \
  source activate symbench-athens-client-dev && \
  python setup.py install && \
  addgroup -S anaconda && \
  adduser -D -u 10151 anaconda -G anaconda && \
  echo "source activate symbench-athens-client-dev" >> \
  /home/anaconda/.profile && \
  mkdir /home/anaconda/data && \
  conda clean -afy && \
  chown -R anaconda:anaconda /symbench-athens-client && \
  chown -R anaconda:anaconda /opt && \
  chown -R anaconda:anaconda /home/anaconda && \
  chown -R anaconda:anaconda /home/anaconda/data

WORKDIR /symbench-athens-client

RUN source activate symbench-athens-client-dev && \
    git clone https://github.com/symbench/uav-analysis.git && \
    cd uav-analysis && python -m pip install -e . && python -m pip install sympy==1.5

RUN python bin/install_fdm.py ${GITLAB_TOKEN}

WORKDIR /home/anaconda

COPY docker/docker-entrypoint.sh /entrypoint.sh

RUN chmod a+x /entrypoint.sh

USER anaconda

ENTRYPOINT ["/entrypoint.sh"]

CMD ["jupyter"]
