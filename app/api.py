from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="CV Builder API",
    urls_namespace="cv"
)
api.auto_discover_controllers()
