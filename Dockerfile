FROM python:3.6-alpine

LABEL io.whalebrew.config.name        'ofxstatement-lfs'
LABEL io.whalebrew.config.working_dir '$PWD'
LABEL io.whalebrew.config.environment '["OFX_ACCOUNT_ID", "OFX_BANK_ID", "OFX_CURRENCY_ID"]'

COPY requirements.txt /tmp
RUN  pip install -r /tmp/requirements.txt

COPY dist/ofxstatement-lfs*.tar.gz /tmp
RUN  pip install /tmp/ofxstatement-lfs*.tar.gz

ENTRYPOINT ["/usr/local/bin/ofxstatement"]
