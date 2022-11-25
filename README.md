# User Mgt Microservice
<!-- [![codecov](https://codecov.io/gh/MarkTLite/chat-cli-kafka/branch/main/graph/badge.svg?token=D1GG1EUSJL)](https://codecov.io/gh/MarkTLite/chat-cli-kafka)
![Test status](https://github.com/MarkTLite/interfaces-databases/actions/workflows/testcov.yml/badge.svg) -->
![Build Status](https://github.com/MarkTLite/odds-crud-microservice/actions/workflows/heroku_deployer.yaml/badge.svg)

## Description
A microservice for User Auth and Mgt that's part of my sportsbetx microservices project. gRPC and CI/CD added

## Generate python files from .proto
    python -m grpc_tools.protoc -I./protos --python_out=./from_protos --pyi_out=./from_protos --grpc_python_out=./from_protos ./protos/odds_crud.proto