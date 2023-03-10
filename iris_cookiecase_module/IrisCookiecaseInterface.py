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
from os import getcwd, path

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
            cid = int((re.search(r'\d+', str(data[0]))).group(0))
            self.log.info(f"Cookie case module running CaseID: ({cid})")

            template_path = path.join(path.dirname(__file__), "template")
            for note_group in Path(template_path).iterdir():

                if note_group.is_dir():
                    note_group_title = str(note_group).split("/")[-1]
                    note_path = path.join(template_path, note_group_title)
                    ng_id = self._case_note_group_create(cng_name=note_group_title, cid=cid)

                    for note in Path(note_path).iterdir():
                        note_title = str(note).split("/")[-1]
                        if "HOLDER" not in note_title:
                            with open(note) as f:
                                content = f.readlines()

                            note_title = str(note).split("/")[-1]
                            cn_id = self._case_note_create(cn_title=note_title, cid=cid, cngid=ng_id, cncon=content)


        return InterfaceStatus.I2Error(data=data, logs=list(self.message_queue))


    def _case_note_group_create(self, cng_name: str, cid: int):
        ng_id = add_note_group(group_title=cng_name, caseid=cid, userid=1, creationdate='2023-03-06 12:12:12')
        ng_id = int((re.search(r'\d+', str(ng_id))).group(0))
        self.log.info(f'Created note group {cng_name} (id: {ng_id}) for case id {cid}')

        return ng_id


    def _case_note_create(self, cn_title: str, cid: int, cngid: int, cncon: str):  
        cn_id = add_note(note_title=cn_title, creation_date='2023-03-06 12:12:12', caseid=cid, user_id=1, group_id=cngid, note_content=cncon)
        cn_id = int((re.search(r'\d+', str(cn_id))).group(0))
        self.log.info(f'Created a note {cn_title} ID ({cn_id}) for case note group {cngid} under the context of case id {cid}')

        return cn_id