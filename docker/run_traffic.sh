#!/bin/bash

# Run stress-ng to create memory load
stress-ng --vm 2 --vm-bytes 1G --vm-keep --timeout 60s
