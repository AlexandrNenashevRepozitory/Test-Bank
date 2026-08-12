from typing import Optional

import requests
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.configs.config import Config
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
import allure



class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self.crud_requester.post(model)
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated model response: {self.endpoint.value.response_model.__name__}")


        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())


    def get(self, path_param: str = "") -> BaseModel:
        response = requests.get(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}{path_param}",
            headers=self.request_spec
        )

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())


    def delete(self, user_id: int) -> BaseModel:
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())