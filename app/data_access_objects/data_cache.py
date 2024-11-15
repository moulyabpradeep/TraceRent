class DataCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataCache, cls).__new__(cls)
            cls._instance.tenant_categories = []
            cls._instance.property_categories = []
            cls._instance.tenant_preferred_properties = []
        return cls._instance

    def get_preferred_properties(self, tent_cat_id: int) -> list[int]:
        """
        Get a list of preferred property category IDs for a given tenant category ID.
        
        Args:
            tent_cat_id (int): Tenant category ID to filter preferred properties.
        
        Returns:
            list[int]: List of property category IDs preferred by the tenant category.
        """
        preferred_props = [
        pref.prop_cat_id
        for pref in self.tenant_preferred_properties
        if pref.tent_cat_id == tent_cat_id
        ]
        print("Preferred properties list:", preferred_props)  # Debug output
        return preferred_props
