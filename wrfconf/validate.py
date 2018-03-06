from marshmallow import fields, Schema, ValidationError


class MetaSchema(Schema):
    """
    Any metadata needed to document the run.


    """
    pass


class RunInfoSchema(Schema):
    start_date = fields.Str(required=True)
    run_hours = fields.Int(required=True)
    max_dom = fields.Int(required=True)


class DomainSchema(Schema):
    parent_id = fields.List(fields.Int, required=True)
    parent_grid_ratio = fields.List(fields.Int, required=True)
    i_parent_start = fields.List(fields.Int, required=True)
    j_parent_start = fields.List(fields.Int, required=True)
    e_we = fields.List(fields.Int)
    e_sn = fields.List(fields.Int)
    dx = fields.List(fields.Int, required=True)
    dy = fields.List(fields.Int, required=True)
    map_proj = fields.Str(required=True)
    ref_lat = fields.Float(required=True)
    ref_lon = fields.Float(required=True)
    ref_x = fields.Float()
    ref_y = fields.Float()
    truelat1 = fields.Float()
    truelat2 = fields.Float()
    geog_data_res = fields.List(fields.Str)


class NamelistSchema(Schema):
    pass


class WPSSchema(Schema):
    pass


class ConfigSchema(Schema):
    meta = fields.Nested(MetaSchema)
    run_info = fields.Nested(RunInfoSchema, required=True)
    domain = fields.Nested(DomainSchema, required=True)
    namelist = fields.Nested(NamelistSchema)
    wps = fields.Nested(MetaSchema)


def validate_config(cfg):
    """
    Validate a yaml configuration file

    There are a number of required and optional parameters. Note that this function does not check every combination of WRF parameters.
    :param cfg:
    :return:
    """
    schema = ConfigSchema()
    try:
        schema.load(cfg)
        return True, []
    except ValidationError as err:
        errors = err.messages
        return False, errors
