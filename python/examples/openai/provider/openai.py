import logging
from collections.abc import Mapping

from dify_plugin.core.runtime.entities.model_runtime.errors import CredentialsValidateFailedError
from dify_plugin.model.model import ModelProvider
from dify_plugin.model.model_entities import ModelType

logger = logging.getLogger(__name__)


class OpenAIProvider(ModelProvider):

    def validate_provider_credentials(self, credentials: Mapping) -> None:
        """
        Validate provider credentials
        if validate failed, raise exception

        :param credentials: provider credentials, credentials form defined in `provider_credential_schema`.
        """
        try:
            model_instance = self.get_model_instance(ModelType.LLM)

            # Use `gpt-3.5-turbo` model for validate,
            # no matter what model you pass in, text completion model or chat model
            model_instance.validate_credentials(
                model='gpt-3.5-turbo',
                credentials=credentials
            )
        except CredentialsValidateFailedError as ex:
            raise ex
        except Exception as ex:
            logger.exception(f'{self.get_provider_schema().provider} credentials validate failed')
            raise ex