from typing import List, Any
from dsframework.base.common.component import ZIDS_Component
import torch
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
        self.model = self.artifacts.model
        self.tokenizer = self.artifacts.tokenizer
        self.adapter_list = self.artifacts.adapter_list

    def predict_by_adapters(self, text:str='', adapters_to_run=None):
        

        tokens = self.tokenizer.tokenize(text)
        input_ids = torch.tensor(self.tokenizer.convert_tokens_to_ids(tokens))
        outputs = self.model(input_ids)

        adapter_list = list(self.adapter_list.keys())
        adapters_to_run = adapter_list if not adapters_to_run else [k for k in adapter_list if k in adapters_to_run]

        prediction = {}
        for adapter_key in adapters_to_run:
            adapter = self.adapter_list[adapter_key]
            labels = self.model.get_labels_dict(adapter)
            index  = adapter_list.index(adapter_key)
            label_id = torch.argmax(outputs[index].logits).item()
            label = labels[label_id]
            prob = torch.nn.functional.softmax(outputs[index].logits, dim=1)[0][label_id].item()
            prediction[adapter_key] = {'pred':label, 'prob':prob}
            
        return prediction

    def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
        for p in predictables:
            p.prediction = self.predict_by_adapters(p.text)
            # prediction = self.cls(p.text)[-1]
            p.pred = any(p.prediction[k]['pred'] in ['Block', 'Negative'] for k in p.prediction.keys())
            p.prob = min([p.prediction[k]['prob'] for k,v in p.prediction.items()])
            p.label = 'Block' if p.pred else 'Allow'
        return predictables
