from .model_db.crud import create_ml_model, get_ml_model, get_all_models
from .model_db.db_setup import Base, SessionLocal, engine

# Spin up DB
Base.metadata.create_all(bind=engine)


class InferenceException(Exception):
    pass


class ModelException(Exception):
    pass


class ModelManager:
    """
    Model Manager class for loading, managing, and interacting with models
    class that instantiates and manages model objects.
    """

    def __init__(self):
        self.__models = []

    def register_model(
        self, model_name: str, model_path: str, inference_path: str
    ) -> None:
        """save the model metadata into model registry"""
        db = SessionLocal()
        if get_ml_model(db, model_name):
            raise ModelException("Model with the same already register")
        else:
            create_ml_model(db, model_name, model_path, inference_path)
            # update_model_list_in_config(MODEL_CONFIG_PATH, [model_name])
        db.close()

    def load_models(self):
        """Load models from configuration."""
        db = SessionLocal()
        try:
            self.__models = []  # resetting the model list to empty
            models = {}
            for model in get_all_models(db):
                self.__models.append(model)
                models[model.name] = {
                    "model_path": model.model_path,
                    "inference_path": model.inference_path,
                }
        except Exception as e:
            raise ModelException("Cannot get models from db", e)
        finally:
            db.close()

    # def get_model_metadata(self, model_name: str) -> tuple[str, str]:
    #     """output model metadata associated with the given model name"""
    #     repo = load_model_repo_from_yaml(MODEL_REPO_PATH)
    #     if model_name in repo:
    #         return repo[model_name]["model_path"], repo[model_name]["inference_path"]
    #     else:
    #         print(f"{model_name} not found in current model registry")
    #     return "", ""

    # @classmethod
    # def get_model_metadata_2(cls, qualified_name: str) -> Optional[Dict[str, Any]]:
    #     """Get a model metadata by qualified name."""
    #     # searching the list of model objects to find the one with the right qualified name
    #     model_objects = [
    #         model for model in cls.__models if model.qualified_name == qualified_name
    #     ]

    #     if len(model_objects) == 0:
    #         return None
    #     else:
    #         model_object = model_objects[0]
    #         return {
    #             "display_name": model_object.display_name,
    #             "qualified_name": model_object.qualified_name,
    #             "description": model_object.description,
    #             "major_version": model_object.major_version,
    #             "minor_version": model_object.minor_version,
    #             "input_schema": model_object.input_schema.to_json_schema(),
    #             "output_schema": model_object.output_schema.to_json_schema(),
    #         }

    # def get_models(self):
    #     return self.__models
    # def get_model(self, model_name: str) -> Optional[Model]:
    #     """Get a model object by qualified name."""
    #     # searching the list of model objects to find the one with the right qualified name
    #     model_objects = [
    #         model for model in self.__models if model.model_name == model_name
    #     ]

    #     if len(model_objects) == 0:
    #         return None
    #     else:
    #         return model_objects[0]
