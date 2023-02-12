#!/usr/bin/env python
# coding: utf-8

from pydantic.main import BaseModel
from typing import Optional
##
# @file
# @brief Setting the output schema of the pipeline / service.
#        What are the expected variables to output?

class PrivacyClassifierOutputs(BaseModel):
    pred: bool
    prob: float
    version: Optional[str] = '0.1'
