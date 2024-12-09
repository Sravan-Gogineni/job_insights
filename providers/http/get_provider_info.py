# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# NOTE! THIS FILE IS AUTOMATICALLY GENERATED AND WILL BE
# OVERWRITTEN WHEN PREPARING PACKAGES.
#
# IF YOU WANT TO MODIFY THIS FILE, YOU SHOULD MODIFY THE TEMPLATE
# `get_provider_info_TEMPLATE.py.jinja2` IN the `dev/breeze/src/airflow_breeze/templates` DIRECTORY


def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-http",
        "name": "Hypertext Transfer Protocol (HTTP)",
        "description": "`Hypertext Transfer Protocol (HTTP) <https://www.w3.org/Protocols/>`__\n",
        "state": "ready",
        "source-date-epoch": 1731570291,
        "versions": [
            "4.13.3",
            "4.13.2",
            "4.13.1",
            "4.13.0",
            "4.12.0",
            "4.11.1",
            "4.11.0",
            "4.10.1",
            "4.10.0",
            "4.9.1",
            "4.9.0",
            "4.8.0",
            "4.7.0",
            "4.6.0",
            "4.5.2",
            "4.5.1",
            "4.5.0",
            "4.4.2",
            "4.4.1",
            "4.4.0",
            "4.3.0",
            "4.2.0",
            "4.1.1",
            "4.1.0",
            "4.0.0",
            "3.0.0",
            "2.1.2",
            "2.1.1",
            "2.1.0",
            "2.0.3",
            "2.0.2",
            "2.0.1",
            "2.0.0",
            "1.1.1",
            "1.1.0",
            "1.0.0",
        ],
        "dependencies": [
            "apache-airflow>=2.8.0",
            "requests>=2.27.0,<3",
            "requests-toolbelt>=0.4.0",
            "aiohttp>=3.9.2,<3.11.0",
            "asgiref>=2.3.0",
        ],
        "integrations": [
            {
                "integration-name": "Hypertext Transfer Protocol (HTTP)",
                "external-doc-url": "https://www.w3.org/Protocols/",
                "how-to-guide": ["/docs/apache-airflow-providers-http/operators.rst"],
                "logo": "/integration-logos/http/HTTP.png",
                "tags": ["protocol"],
            }
        ],
        "operators": [
            {
                "integration-name": "Hypertext Transfer Protocol (HTTP)",
                "python-modules": ["airflow.providers.http.operators.http"],
            }
        ],
        "sensors": [
            {
                "integration-name": "Hypertext Transfer Protocol (HTTP)",
                "python-modules": ["airflow.providers.http.sensors.http"],
            }
        ],
        "hooks": [
            {
                "integration-name": "Hypertext Transfer Protocol (HTTP)",
                "python-modules": ["airflow.providers.http.hooks.http"],
            }
        ],
        "triggers": [
            {
                "integration-name": "Hypertext Transfer Protocol (HTTP)",
                "python-modules": ["airflow.providers.http.triggers.http"],
            }
        ],
        "connection-types": [
            {"hook-class-name": "airflow.providers.http.hooks.http.HttpHook", "connection-type": "http"}
        ],
    }
