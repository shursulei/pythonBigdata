#!/usr/bin/env bash
kill -9 `ps -ef|grep TaskTimer |grep -v grep |awk '{print $2}'`