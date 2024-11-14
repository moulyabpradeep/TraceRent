
#TODO: rewrite 3 quires : delete-disliked,liked,disliked
DELETE_DISLIKED_PROPERTIES_QUERY = f""" """
GET_LIKED_PROPERTIES_QUERY = f""" """
GET_DISLIKED_PROPERTIES_QUERY = f""" """


# db_queries.py

UPSERT_TENANT_PREFERENCES = """
INSERT INTO tenant_preference_details (
    user_id, session_id, tenant_category_id, location_category_id, budget_category_id,
    school_proximity, hospital_proximity, transit_proximity, in_house_laundry,
    gym, pet_friendly, pool, is_logged_in
)
VALUES (
    COALESCE(:user_id, NULL), :session_id, :tenant_category_id, :location_category_id, :budget_category_id,
    :school_proximity, :hospital_proximity, :transit_proximity, :in_house_laundry,
    :gym, :pet_friendly, :pool, :is_logged_in
)
ON DUPLICATE KEY UPDATE
    tenant_category_id = VALUES(tenant_category_id),
    location_category_id = VALUES(location_category_id),
    budget_category_id = VALUES(budget_category_id),
    school_proximity = VALUES(school_proximity),
    hospital_proximity = VALUES(hospital_proximity),
    transit_proximity = VALUES(transit_proximity),
    in_house_laundry = VALUES(in_house_laundry),
    gym = VALUES(gym),
    pet_friendly = VALUES(pet_friendly),
    pool = VALUES(pool),
    is_logged_in = VALUES(is_logged_in),
    user_id = IF(VALUES(user_id) IS NOT NULL, VALUES(user_id), user_id),
    session_id = IF(VALUES(is_logged_in) = FALSE, VALUES(session_id), session_id);
"""