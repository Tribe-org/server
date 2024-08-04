#!/bin/bash

# 현재 브랜치 이름 가져오기
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo $CURRENT_BRANCH

TICKET=$(echo $CURRENT_BRANCH | awk -F '/' '{ print $2 }' | tr '[a-z]' '[A-Z]')
echo $TICKET

CURRENT_MSG=$(git log -1)
echo $CURRENT_MSG