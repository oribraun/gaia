#!/usr/bin/env python
# coding: utf-8

import json
from dsframework.base.pipeline.artifacts.shared_artifacts import ZIDS_SharedArtifacts
from transformers import RobertaTokenizer, RobertaConfig, RobertaAdapterModel
from transformers import TextClassificationPipeline

"""! @brief PrivacyClassifierSharedArtifacts (SharedArtifacts) class."""
class PrivacyClassifierSharedArtifacts(ZIDS_SharedArtifacts):

    def __init__(self) -> None:
        """! @brief PrivacyClassifierSharedArtifacts (SharedArtifacts) class.

        Override ZIDS_SharedArtifacts methods here, such as extend_load_file_type() for loading new file types.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__()
        self.adapters_path = ''
        self.privacy_adapters_classifier = None
        self.load_adapters()

    def extend_load_file_type(self, file_type, path, absolute_path, name):
        if absolute_path:
            if file_type == 'your-file-type':
                with open(absolute_path) as json_file:
                    setattr(self, name, json.load(json_file))

    def load_adapters(self):
        self.adapters_path = f'{self.base_dir}pipeline/artifacts/adapters'


        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

        config = RobertaConfig.from_pretrained(
            "roberta-base",
            num_labels=2,
        )

        model = RobertaAdapterModel.from_pretrained(
            "roberta-base",
            config=config,
        )

        rt_adapter = model.load_adapter(f'{self.adapters_path}/temp_adapter')
        model.set_active_adapters(rt_adapter)
        self.privacy_adapters_classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)