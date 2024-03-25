#!/bin/bash
docker build -t test-app-container -f DockerfileTest  .
docker run test-app-container