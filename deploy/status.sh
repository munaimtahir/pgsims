#!/usr/bin/env bash
set -euo pipefail

PROJECT="pgsims"
docker ps --filter "label=com.docker.compose.project=$PROJECT"
