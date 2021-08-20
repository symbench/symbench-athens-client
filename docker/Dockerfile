FROM continuumio/miniconda3:4.8.2-alpine AS builder

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
    apk add alpine-sdk && \
    apk add gfortran && \
    apk add automake=1.16.1-r0 && \
    apk add autoconf

WORKDIR /symbench-athens-client

RUN conda update conda -yq && \
  conda config --set always_yes yes --set changeps1 no && \
  . /opt/conda/etc/profile.d/conda.sh && \
  conda install -c conda-forge mamba && \
  mamba env create nomkl --file environment-docker.yml && \
  source activate symbench-athens-client-dev && \
  python setup.py install && \
  echo "source activate symbench-athens-client-dev" >> \
  /home/anaconda/.profile && \
  conda clean -afy && \
  mkdir /home/anaconda/data && \
  chown -R anaconda:anaconda /symbench-athens-client && \
  chown -R anaconda:anaconda /opt && \
  chown -R anaconda:anaconda /home/anaconda

WORKDIR /symbench-athens-client

RUN python bin/install_fdm.py ${GITLAB_TOKEN}

WORKDIR /home/anaconda

COPY docker/docker-entrypoint.sh /entrypoint.sh

RUN chmod a+x /entrypoint.sh

USER anaconda

ENTRYPOINT ["/entrypoint.sh"]

CMD ["jupyter"]