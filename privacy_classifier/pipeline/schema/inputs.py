#!/usr/bin/env python
# coding: utf-8

from pydantic.main import BaseModel
from typing import Optional,Any

##
# @file
# @brief Setting the schema inputs, which is the basic structure that the pipeline/service would receive.
#        What data variables you need as an input? it could be a dataset or part of it and additional required variables, such as threshold etc.
#        Using Pydantic's base class that can validate their input class.

class PrivacyClassifierInputs(BaseModel):

    text:str
    hints:Optional[Any] = None
