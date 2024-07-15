import os
from abc import abstractmethod
from typing import IO, Optional

from pydantic import ConfigDict

from dify_plugin.model.ai_model import AIModel
from dify_plugin.model.model_entities import ModelType



class Speech2TextModel(AIModel):
    """
    Model class for speech2text model.
    """
    model_type: ModelType = ModelType.SPEECH2TEXT

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())

    def invoke(self, model: str, credentials: dict,
               file: IO[bytes], user: Optional[str] = None) \
            -> str:
        """
        Invoke large language model

        :param model: model name
        :param credentials: model credentials
        :param file: audio file
        :param user: unique user id
        :return: text for given audio file
        """
        try:
            return self._invoke(model, credentials, file, user)
        except Exception as e:
            raise self._transform_invoke_error(e)

    @abstractmethod
    def _invoke(self, model: str, credentials: dict,
                file: IO[bytes], user: Optional[str] = None) \
            -> str:
        """
        Invoke large language model

        :param model: model name
        :param credentials: model credentials
        :param file: audio file
        :param user: unique user id
        :return: text for given audio file
        """
        raise NotImplementedError

    def _get_demo_file_path(self) -> str:
        """
        Get demo file for given model

        :return: demo file
        """
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the audio file
        return os.path.join(current_dir, 'audio.mp3')