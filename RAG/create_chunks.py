"""This module provides functions to create text chunks with metadata from service data."""

def create_chunks_with_metadata(centre_data):
    """
    Create text chunks with metadata from the provided centre data.

    Args:
        centre_data (list): A list of dictionaries containing centre and group data for a service
    Returns:
        list: A list of dictionaries, each containing a text chunk and its associated metadata.
    """
    chunks_with_metadata = []
    chunks_with_metadata.append(create_centre_chunks(centre_data))

    for group in centre_data.get('weekly_groups', []):
        chunks_with_metadata.append(create_group_chunks(group, centre_data))
        
    return chunks_with_metadata



def create_centre_chunks(centre_data):
    """
    Create a text chunk with metadata for a service centre.

    Args:
        centre_data (list): A list of dictionaries containing centre and group data for a service  
    Returns:
        dict: A dictionary containing the text chunk and its associated metadata.
    """
    text = (
        f"{centre_data['service_name']} is located at {centre_data['address']}. "
        f"It is open {centre_data['opening_hours']}. Services offered include: "
        f"{', '.join(centre_data['services'])}."
        f"You can contact the {centre_data['service_name']} by calling {centre_data['phone']} "
        f"or emailing {centre_data['email']}."
    )
    metadata = {
        "type": "centre_info",  
        "source": "centre",
        "service_name": centre_data.get('service_name', []),  
        "location": centre_data.get('location', []),
        "address": centre_data.get('address', []),
        "email": centre_data.get('email', []),
        "phone": centre_data.get('phone', []),
        "opening_hours": centre_data.get('opening_hours', [])
    }
    return {'text':text ,'metadata': metadata}


def create_detailed_group_chunks(group, centre_data):
    """ Subfunction to create detailed text chunks for a group.
    Args:
        group (dict): A dictionary containing information about the group.
        centre_data (list): A list of dictionaries containing centre and group data for a service   
    Returns:
        dict: A dictionary containing the text chunk and its associated metadata.
    """
    text = (
        f"The '{group['name']}' runs at the {centre_data['service_name']} centre on {group['day']}s at {group['time']}."
    )
    if 'duration' in group:
        text += f" It runs for {group['duration']}."
    if group.get('registration_required'):
        text += " Registration is required."

    if 'description' in group:
        text += f" About the group: {group['description']}"

    if 'topics' in group and group['topics']:
        topic_text = " Topics covered include: " + "; ".join(group['topics']) + "."
        text += topic_text

    if 'who_is_it_for' in group:
        text += f" This group is suitable for: {group['who_is_it_for']}"

    metadata = {
        "type": "detailed_group_info",
        "source": "weekly_group",
        "service_name": centre_data.get('service_name', []),
        "location": centre_data.get('location', []),
        "address": centre_data.get('address', []),
        "email": centre_data.get('email', []),
        "phone": centre_data.get('phone', []),
        "opening_hours": centre_data.get('opening_hours', []),
        "group_name": group.get('name', []),
        "day": group.get('day', []),
        "time": group.get('time', []),
        "duration": group.get('duration', []),
        "registration_required": group.get('registration_required', [])
    }
    
    return {'text':text ,'metadata': metadata}


def create_group_chunks(group, centre_data):   
    """
    Create a text chunk with metadata for a weekly group.
    Args:
        group (dict): A dictionary containing information about the group.
        centre_data (list): A list of dictionaries containing centre and group data for a service
    Returns:
        dict: A dictionary containing the text chunk and its associated metadata.
    """
    if any(k in group for k in ['topics', 'description', 'who_is_it_for']):
        return create_detailed_group_chunks(group, centre_data)

    text = (
        f"The {group['name']} meets at the {centre_data['service_name']} every {group['day']} from {group['time']}."
    )
    if "link" in group:
        text += f" Find out more here: {group['link']}"

    if group["day"] == "TBC" or "on hold" in group["time"].lower():
        text = (
            f"The {group['name']} at the {centre_data['service_name']} is currently on hold. "
            f"It is expected to return later, likely in the spring."
        )

    metadata = {
        "type": "group_info",
        "source": "weekly_group",
        "service_name": centre_data.get('service_name', []),
        "location": centre_data.get('location', []),
        "address": centre_data.get('address', []),
        "email": centre_data.get('email', []),
        "phone": centre_data.get('phone', []),
        "opening_hours": centre_data.get('opening_hours', []),
        "group_name": group.get('name', []),
        "day": group.get('day', []),
        "time": group.get('time', [])
    }
    
    return {'text':text ,'metadata': metadata}







