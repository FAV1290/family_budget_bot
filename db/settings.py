from db.database_init import db_session
from db.database_models import Settings
from apps.converters import convert_settings_object_to_dict


def update_utc_offset(target_id, new_utc_offset):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None:
        new_settings_object = Settings(
            user_id = target_id,
            is_app_configured = False,
            utc_offset = new_utc_offset
        )
        db_session.add(new_settings_object)
    else:
        settings_object.utc_offset = new_utc_offset
    db_session.commit()


def update_config_status(target_id, new_status):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None:
        new_settings_object = Settings(
            user_id = target_id,
            is_app_configured = new_status,
            utc_offset = 0     
        )
        db_session.add(new_settings_object)
    else:
        settings_object.is_app_configured = new_status
    db_session.commit() 


def get_user_settings(target_id):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None:
        settings_object = Settings(
            user_id = target_id,
            is_app_configured = False,
            utc_offset = 0
        )
    return convert_settings_object_to_dict(settings_object)
