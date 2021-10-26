[![Build and push image](https://github.com/PHT-Medic/central-email-service/actions/workflows/CI.yml/badge.svg)](https://github.com/PHT-Medic/central-email-service/actions/workflows/CI.yml)
[![CodeQL](https://github.com/PHT-Medic/central-email-service/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/PHT-Medic/central-email-service/actions/workflows/codeql-analysis.yml)
[![Vulnerability Scan](https://github.com/PHT-Medic/central-email-service/actions/workflows/image_scan.yml/badge.svg)](https://github.com/PHT-Medic/central-email-service/actions/workflows/image_scan.yml)


# PHT Email Service

PHT Email Service is implementing a microservice listening to rabbitmq messages and sending out email notifications to the station admins regarding new trains that can be approved or ready for a station to execute.

## Setup

In docker-compose.yml set the variables for the UI API , the mqrabbid url AMPQ_URL in the form
amqp://<user>:<user_password>@ip_address:port/ and the data for a smtp server and user.

      - UI_TRAIN_API=
      - AMPQ_URL=
      - SMTP_USER=
      - SMTP_PASSWORD=
      - UI_USER=
      - UI_TOKEN=
      - UI_ADDRESS=
      - SMTP_MAIL_FROM=
      - SMTP_HOST=

Then build the train with `docker-compose build` and start the service `docker-compose up -d` . 
