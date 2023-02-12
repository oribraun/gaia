# !/usr/bin/env python
# coding: utf-8

from typing import List, Any

from dsframework.base.pipeline.preprocessor import ZIDS_Preprocessor
from ..schema.inputs import PrivacyClassifierInputs
from ..schema.outputs import PrivacyClassifierOutputs
from ..artifacts.shared_artifacts import PrivacyClassifierSharedArtifacts
from ..predictables import PrivacyClassifierPredictable

##
# @file
# @brief PrivacyClassifierPreprocess (Preprocess) class, implements ZIDS_Preprocessor base class.
class PrivacyClassifierPreprocess(ZIDS_Preprocessor):
    """! PrivacyClassifierPreprocess (Preprocessor) class implements ZIDS_Preprocessor base class.

    First step of the pipeline, its main goal is to format the dataset format to the model requirements.

    Its base class ZIDS_Preprocessor declares phases based on UVM (Universal Verification Methodology) and by this it
    gives us a structured way to work in each one of the main components by overriding and implementing those phases
    in this class.

    Important note:
    Those methods are divided into two groups, the ones that run from the ZIDS_Component.__init__() and
    those that run from ZIDS_Component.execute() method, use them based on the required execution order.

    In the __init__() we have the following called:
    - build
    - config
    - config_from_json
    - connect

    In the execute(), we call the following:
    - reset
    - pre_run
    - run
    - post_run
    - evaluate
    """

    def __init__(self, artifacts: PrivacyClassifierSharedArtifacts = None):
        """! PrivacyClassifierPreprocess (Preprocess) initializer

        Args:
            artifacts(PrivacyClassifierSharedArtifacts): Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)

    def normalize_input(self, **kwargs: Any) -> PrivacyClassifierInputs:
        """! Converts dataset to PrivacyClassifierInputs

        Args:
            **kwargs: Loaded dataset.
        Returns:
            The loaded dataset in PrivacyClassifierInputs datatype.
        """
        return PrivacyClassifierInputs(**kwargs)

    def config(self):
        """! Config method called from ZIDS_Component.__init__()

        Method not implemented, ready for your implementation, see more information in class description.
        """
        pass

    def reset(self, raw_input: Any):
        self.text = raw_input.text
        self.hints = raw_input.hints
        self.splitted = []
        self._split_text()

    def _split_text(self):
        self.splitted = self.text.strip().split('\n\n')

    def preprocess(self, raw_input: Any):
        """! Implement method to return a list of predictable objects.

        Args:
            raw_input: input to the pipeline, after normalization.

        Returns:
            List[ZIDS_Predictable] - Not implemented yet.

        Raises:
            NotImplementedError
        """
        self.reset(raw_input)

        return [PrivacyClassifierPredictable(text = t) for t in self.splitted]
         
