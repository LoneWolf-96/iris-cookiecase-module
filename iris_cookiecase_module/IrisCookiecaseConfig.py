#!/usr/bin/env python3
#
#
#  IRIS cookiecase Source Code
#  Copyright (C) 2023 - iris-cookiecase-module
#  coding.LoneWolf-96@proton.me
#  Created by iris-cookiecase-module - 2023-03-06
#
#  License MIT

module_name = "IrisCookiecase"
module_description = "Iris Cookie Case is designed to standardise all new cases created in DFIR IRIS, ensuring they all automatically contain the core note groups and notes."
interface_version = 1.1
module_version = 1.0

pipeline_support = False
pipeline_info = {}


module_configuration = [
    {
        "param_name": "cookie_make_case",
        "param_human_name": "Cookie cutter case",
        "param_description": "Cookie a case, so they are all uniformed to start with.",
        "default": True,
        "mandatory": True,
        "type": "bool"
    }
]