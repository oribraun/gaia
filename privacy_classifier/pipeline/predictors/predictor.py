from typing import List, Any
from dsframework.base.common.component import ZIDS_Component

##
# @file
# @brief Predictor class, this is where the model goes.

class PrivacyClassifierPredictor(ZIDS_Component):
    """! PrivacyClassifierPredictor class (Predictor) implements ZIDS_Component base class.

    The second step of the pipeline and its main goal is to feed a dataset to a model.

    All the action happens in this step, model sits in this class.
    """

    def __init__(self, artifacts=None) -> None:
        """PrivacyClassifierPredictor class (Postprocessor) initializer

        Args:
            artifacts: Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)
        self.cls = self.artifacts.privacy_adapters_classifier

    def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
        for p in predictables:
            prediction = self.cls(p.text)[-1]
            p.pred = 'Negative' if '0' in prediction['label'] else 'Positive'
            p.prob = prediction['score']
            p.label = prediction['label']
        return predictables
