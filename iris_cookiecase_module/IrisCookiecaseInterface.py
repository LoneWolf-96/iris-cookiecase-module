#!/usr/bin/env python3
#
#
#  IRIS cookiecase Source Code
#  Copyright (C) 2023 - iris-cookiecase-module
#  hello@iris-cookiecase-module.com
#  Created by iris-cookiecase-module - 2023-03-06
#
#  License MIT

import traceback
import re
from pathlib import Path

import iris_interface.IrisInterfaceStatus as InterfaceStatus
from iris_interface.IrisModuleInterface import IrisPipelineTypes, IrisModuleInterface, IrisModuleTypes
from app.datamgmt.case.case_notes_db import add_note_group, add_note

import iris_cookiecase_module.IrisCookiecaseConfig as interface_conf


class IrisCookiecaseInterface(IrisModuleInterface):
    """
    Provide the interface between Iris and cookiecaseHandler
    """
    name = "IrisCookiecaseInterface"
    _module_name = interface_conf.module_name
    _module_description = interface_conf.module_description
    _interface_version = interface_conf.interface_version
    _module_version = interface_conf.module_version
    _pipeline_support = interface_conf.pipeline_support
    _pipeline_info = interface_conf.pipeline_info
    _module_configuration = interface_conf.module_configuration
    
    _module_type = IrisModuleTypes.module_processor
    
     
    def register_hooks(self, module_id: int):
        """
        Registers all the hooks

        :param module_id: Module ID provided by IRIS
        :return: Nothing
        """
        self.module_id = module_id
        module_conf = self.module_dict_conf
        if module_conf.get('check_log_received_hook'):
            status = self.register_to_hook(module_id, iris_hook_name='on_postload_case_create')
            if status.is_failure():
                self.log.error(status.get_message())
                self.log.error(status.get_data())

            else:
                self.log.info("Successfully registered on_postload_case_create hook")
        else:
            self.deregister_from_hook(module_id=self.module_id, iris_hook_name='on_postload_case_create')



    def hooks_handler(self, hook_name: str, hook_ui_name: str, data: any):
        """
        Hooks handler table. Calls corresponding methods depending on the hooks name.

        :param hook_name: Name of the hook which triggered
        :param hook_ui_name: Name of the ui hook
        :param data: Data associated with the trigger.
        :return: Data
        """

        self.log.info(f'Received {hook_name}')

        if hook_name in ['on_postload_case_create']:
            # Extract the Case ID from the data type
            cid = re.search(r'\d+', str(data[0]))
            cid = int(cid.group(0))
            self.log.info(f"Cookie case module running CaseID: ({cid})")
            
            return InterfaceStatus.I2Error(data=data, logs=list(self.message_queue))