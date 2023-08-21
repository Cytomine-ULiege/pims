ARG NAMESPACE
ARG VERSION

FROM ${NAMESPACE}/pims:${VERSION}

COPY tests /app/tests

RUN pip install pytest

WORKDIR /app

CMD ["pytest", "tests", "--junit-xml=test-report.xml"]
