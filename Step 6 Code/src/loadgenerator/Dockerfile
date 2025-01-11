# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.12.6-slim@sha256:ad48727987b259854d52241fac3bc633574364867b8e20aec305e6e7f4028b26 AS base

FROM base AS builder

COPY requirements.txt .

RUN pip install --prefix="/install" -r requirements.txt

FROM base

WORKDIR /loadgen

COPY --from=builder /install /usr/local

# Add application code.
COPY locustfile.py .

# enable gevent support in debugger
ENV GEVENT_SUPPORT=True

ENTRYPOINT bash -c "locust --host='http://34.41.49.23' --headless -u '${USERS:-100}' -r 10 -t 3m --csv=loadgenerator 2>&1 ; apt-get update && apt-get install -y awscli && mv loadgenerator_stats.csv \"loadgenerator_stats_$(date +%Y-%m-%d_%H-%M-%S).csv\" && mv loadgenerator_stats_history.csv \"loadgenerator_stats_history_$(date +%Y-%m-%d_%H-%M-%S).csv\" && mv loadgenerator_failures.csv \"loadgenerator_failures_$(date +%Y-%m-%d_%H-%M-%S).csv\" && mv loadgenerator_exceptions.csv \"loadgenerator_exceptions_$(date +%Y-%m-%d_%H-%M-%S).csv\" && aws s3 cp ./ s3://cloudlabapolidockefile/CSVs --recursive --exclude \"*\" --include \"*.csv\""
