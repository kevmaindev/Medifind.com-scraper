def safe_get(dictionary, *keys):
    """Safely get a value from a nested dictionary with list support."""
    current = dictionary
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
            current = current[key]
        else:
            return None
    return current

def get_doc_data(data):
    # Basic Info
    doc_id = safe_get(data, "docId")
    name = safe_get(data, "name")
    display_name = safe_get(data, "displayName")
    display_name_short = safe_get(data, "displayNameShort")
    initials = safe_get(data, "initials")
    family_name = safe_get(data, "familyName")

    # Address Info
    address_line1 = safe_get(data, "address", "addressLine1")
    address_line2 = safe_get(data, "address", "addressLine2")
    city = safe_get(data, "address", "city")
    state_province = safe_get(data, "address", "stateProvince")
    state_province_code = safe_get(data, "address", "stateProvinceCode")
    country_2_code = safe_get(data, "address", "country2Code")
    country = safe_get(data, "address", "country")
    postal_code = safe_get(data, "address", "postalCode")
    location_string = safe_get(data, "address", "locationString")
    location = safe_get(data, "address", "location")
    static_map_alt = safe_get(data, "address", "staticMapAlt")

    # Geolocation Info
    latlon = safe_get(data, "address", "latlon")
    distance = safe_get(data, "address", "distance")
    lat = safe_get(data, "address", "lat")
    lon = safe_get(data, "address", "lon")
    fidelity = safe_get(data, "address", "fidelity")

    # Organization Info
    org_phone_number = safe_get(data, "address", "orgPhoneNumber")
    org_name = safe_get(data, "address", "orgName")
    primary_org_name = safe_get(data, "primaryOrgName")

    # Contact Info
    phone = safe_get(data, "phone")
    appointment_phone = safe_get(data, "appointmentPhone")

    # Professional Info
    is_us_prescriber = safe_get(data, "isUSPrescriber")
    specialties = safe_get(data, "specialties")
    primary_specialty = safe_get(data, "primarySpecialtyLookup", "specialty")
    primary_specialty_slug = safe_get(data, "primarySpecialtyLookup", "slug")
    primary_specialty_role = safe_get(data, "primarySpecialtyLookup", "role")
    years_of_experience = safe_get(data, "yearsOfExperience")
    is_doctor = safe_get(data, "isDoctor")
    highly_rated_conditions_count = safe_get(data, "highlyRatedConditionsCount")
    coding_count = safe_get(data, "codingCount")

    # Demographic Info
    sex = safe_get(data, "demographics", "sex")
    languages = safe_get(data, "languages")

    # Credentials
    credential_codes = safe_get(data, "credentialCodes")
    licenses = safe_get(data, "credentials", "licenses")

    # Affiliations
    practice_affiliations = safe_get(data, "affiliations", "practice")
    hospital_affiliations = safe_get(data, "affiliations", "hospitals")

    # Additional Info
    biography = safe_get(data, "biography")

    # Badges
    badges_roles = safe_get(data, "badges", "roles")
    badges_awards = safe_get(data, "badges", "awards")
    badges_fellowships = safe_get(data, "badges", "fellowships")

    # Issuers
    issuers = safe_get(data, "issuers") or []
    processed_issuers = []
    for i, issuer in enumerate(issuers, 1):
        issuer_data = {
            f"issuer_{i}_name": issuer.get("issuerName"),
            f"issuer_{i}_personify_id": issuer.get("personifyId")
        }
        processed_issuers.append(issuer_data)

    # Flat dictionary
    provider_data = {
        "doc_id": doc_id,
        "name": name,
        "display_name": display_name,
        "display_name_short": display_name_short,
        "initials": initials,
        "family_name": family_name,
        
        "address_line1": address_line1,
        "address_line2": address_line2,
        "city": city,
        "state_province": state_province,
        "state_province_code": state_province_code,
        "country_2_code": country_2_code,
        "country": country,
        "postal_code": postal_code,
        "location_string": location_string,
        "location": location,
        "static_map_alt": static_map_alt,
        
        "latlon": latlon,
        "distance": distance,
        "lat": lat,
        "lon": lon,
        "fidelity": fidelity,
        
        "org_phone_number": org_phone_number,
        "org_name": org_name,
        "primary_org_name": primary_org_name,
        
        "phone": phone,
        "appointment_phone": appointment_phone,
        
        "is_us_prescriber": is_us_prescriber,
        "specialties": specialties,
        "primary_specialty": primary_specialty,
        "primary_specialty_slug": primary_specialty_slug,
        "primary_specialty_role": primary_specialty_role,
        "years_of_experience": years_of_experience,
        "is_doctor": is_doctor,
        "highly_rated_conditions_count": highly_rated_conditions_count,
        "coding_count": coding_count,
        
        "sex": sex,
        "languages": languages,
        
        "credential_codes": credential_codes,
        "licenses": licenses,
        
        "practice_affiliations": practice_affiliations,
        "hospital_affiliations": hospital_affiliations,
        
        "biography": biography,
        
        "badges_roles": badges_roles,
        "badges_awards": badges_awards,
        "badges_fellowships": badges_fellowships,
        
    }
    for issuer_dict in processed_issuers:
        provider_data.update(issuer_dict)

    return provider_data
    
def all_docs(data):
    all_docs = []
    for doc in data.get('results'):
        doc_data = get_doc_data(doc)
        all_docs.append(doc_data)
    return all_docs