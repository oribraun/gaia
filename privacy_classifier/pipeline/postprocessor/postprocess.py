 # !/usr/bin/env python
# coding: utf-8

##
# @file
# @brief Postprocessor class, implemented ZIDS_Postprocessor base.

from dsframework.base.pipeline.predictables.predictable import ZIDS_Predictable
from typing import List, Union

from dsframework.base.pipeline.postprocessor import ZIDS_Postprocessor
from ..artifacts.shared_artifacts import PrivacyClassifierSharedArtifacts
from ..schema.outputs import PrivacyClassifierOutputs


class PrivacyClassifierPostprocess(ZIDS_Postprocessor):
    """PrivacyClassifierPostprocess class (Postprocessor) implements ZIDS_Postprocessor base class.
    Last step of the pipeline, its main focus is to return the results in the required format.
    """

    def __init__(self, artifacts: PrivacyClassifierSharedArtifacts = None) -> None:
        """! PrivacyClassifierPostprocess class (Postprocessor) initializer

        Args:
            artifacts(PrivacyClassifierSharedArtifacts): Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)

    def config(self):
        """Implement here configurations required on Preprocess step. Overrides ZIDS_Component.config()"""
        pass

    def normalize_output(self, predictables: Union[ZIDS_Predictable, List[ZIDS_Predictable]]) -> Union[PrivacyClassifierOutputs, List[PrivacyClassifierOutputs]]:
        """! Converts received predictable objects to PrivacyClassifierOutputs datatype.

        Args:
            predictables: List[ZIDS_Predictable] - Predictable objects, the results from the model.

        Returns:
            PrivacyClassifierOutputs: List[PrivacyClassifierOutputs] - Results converted to Outputs format.
        """

        output: PrivacyClassifierOutputs = ''
        isList = isinstance(predictables, list)
        if isList:
            output: List[PrivacyClassifierOutputs] = []
        if isList:
            if predictables and len(predictables):
                for item in predictables:
                    output.append(self.get_output_object(item))
        else:
            output = self.get_output_object(predictables)
        return output

    def get_output_object(self, predictable):
        """! Parse a single predictable item, needs to be implemented.

        Args:
            predictable: ZIDS_Predictable - Single predictable object.

        Returns:
            PrivacyClassifierOutputs: PrivacyClassifierOutputs - Parsed results

        Raises:
            NotImplementedError

        """
        out = {'text':predictable.text, 'pred': predictable.pred, 'prob': predictable.prob}
        return out

