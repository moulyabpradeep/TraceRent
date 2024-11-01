# global_constants.py

# All the constants in the Project will be placed here

# Define table names as constants
TENANT_PERSONAL_DETAILS_TABLE = 'tenant_personal_details'
TENANT_PREFERENCE_DETAILS_TABLE = 'tenant_preference_details'
TENANT_CATEGORY_TABLE = 'tenant_category'
PROPERTY_CATEGORY_TABLE = 'property_category'
TENANT_PREFERRED_PROPERTIES_TABLE = 'tenant_preferred_properties'
PROPERTY_DATA_TABLE = 'property_data'
USER_TABLE = 'user'

# Define column names as constants (keep them here for easy access)
PROP_CAT_ID_COLUMN = 'prop_cat_id'
TENT_CAT_ID_COLUMN = 'tent_cat_id'
# Add other column constants as needed

# Configurable interval (in days)
DAYS_THRESHOLD = 7

DELETE_DISLIKED_PROPERTIES_QUERY = f"""
DELETE FROM {TENANT_PREFERENCE_DETAILS_TABLE}
WHERE is_liked = 0 AND created_at < DATE_SUB(NOW(), INTERVAL :days_threshold DAY)
"""

GET_LIKED_PROPERTIES_QUERY = f"""
SELECT *
FROM {TENANT_PREFERENCE_DETAILS_TABLE}
WHERE user_id = :user_id AND is_liked = 1
"""


GET_DISLIKED_PROPERTIES_QUERY = f"""
SELECT *
FROM {TENANT_PREFERENCE_DETAILS_TABLE}
WHERE user_id = :user_id AND is_liked = 0
"""
