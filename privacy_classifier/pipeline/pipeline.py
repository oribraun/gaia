"""! @brief Pipeline class, implements ZIDS_Pipeline base class."""
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

from dsframework.base.pipeline.pipeline import ZIDS_Pipeline

from .preprocessor.preprocess import PrivacyClassifierPreprocess
from .postprocessor.postprocess import PrivacyClassifierPostprocess
from .predictors.predictor import PrivacyClassifierPredictor
from .forcers.forcer import PrivacyClassifierForcer
from .artifacts.shared_artifacts import PrivacyClassifierSharedArtifacts

##
# @file
# @brief Pipeline main class, implements ZIDS_Pipeline base class.
class PrivacyClassifierPipeline(ZIDS_Pipeline):
    """! Pipeline main class

    Its main job is to build the pipeline components, by default it includes four main components:
    preprocess, predictor, forcer and postprocess.
    """

    def __init__(self):
        """! The PrivacyClassifierPipeline class (Pipeline) initializer."""

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__()

    def get_artifacts(self):
        """! Loads the artifacts and return the results.

        Triggers execution of load_artifacts and load_vocabs on base class ZIDS_SharedArtifacts.
        It overrides ZIDS_Pipeline.get_artifacts.


        Returns:
             PrivacyClassifierSharedArtifacts() - Results of loaded artifacts.

        """
        return PrivacyClassifierSharedArtifacts()

    def build_pipeline(self):
        """! Builds the pipeline.

        Instantiate the default four main components:
        Preprocessor, Predictor, Forcer and Postprocessor.
        """

        ##
        # Additional components can be added using the add_component method, for example:
        # @code
        # self.new_component = PrivacyClassifierNewComponent()
        # self.add_component(self.new_component)
        # @endcode

        ## Instantiate preprocessor - Automatically added to the pipeline
        self.preprocessor = PrivacyClassifierPreprocess(artifacts=self.artifacts)

        ## Instantiate and add predictor to the pipeline
        self.predictor = PrivacyClassifierPredictor()
        self.add_component(self.predictor)

        ## Instantiate and add forcer to the pipeline
        self.forcer = PrivacyClassifierForcer()
        self.add_component(self.forcer)

        ## Instantiate postprocessor - Automatically added to the pipeline
        self.postprocessor = PrivacyClassifierPostprocess(artifacts=self.artifacts)

    def preprocess(self, **kwargs):
        """! Executes preprocessor, called from ZIDS_Pipeline baseclass execute method.

        Args:
            **kwargs : Dataset and additional parameters loaded initially.
        Returns:
            List of predictable objects (PrivacyClassifierInputs datatype)
        """
        return self.preprocessor(**kwargs)

    def postprocess(self, predictables):
        """! Executes the postprocessor, called from ZIDS_Pipeline baseclass execute method.

        Args:
            predictables: List[PrivacyClassifierInputs] - List of predictable objects.
        Returns:
            PrivacyClassifierPostprocess: List[PrivacyClassifierOutputs]: List of results.
        """
        return self.postprocessor(predictables)
