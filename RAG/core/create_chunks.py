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

    for group in centre_data.get('support_groups', []):
        chunks_with_metadata.append(create_group_chunks(group, centre_data))

    for counselling in centre_data.get('counselling_services', []):
        chunks_with_metadata.append(create_counselling_chunks(counselling, centre_data))

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
        f"The {centre_data['location']} centre is located at {centre_data['address']}. "
        f"Services offered include: "
        f"{', '.join(centre_data['services'])}."
        f"You can contact the {centre_data['location']} centre by calling {centre_data['phone']} "
        f"or emailing {centre_data['email']}."
    )
    metadata = {
        "type": "centre_info",  
        "source": "centre",
        "location": centre_data.get('location', []),
        "address": centre_data.get('address', []),
        "email": centre_data.get('email', []),
        "phone": centre_data.get('phone', []),
        "opening_hours": centre_data.get('opening_hours', [])
    }
    return {'text':text ,'metadata': metadata}


def create_group_chunks(group, centre_data):   
    """
    Create a text chunk with metadata for a support group.
    Args:
        group (dict): A dictionary containing information about the group.
        centre_data (list): A list of dictionaries containing centre and group data for a service
    Returns:
        dict: A dictionary containing the text chunk and its associated metadata.
    """

    text = (
        f"The {group['name']} group meets at the {centre_data['location']} every {group['day']} from {group['time']}."
        f"{group['name']} is {group['description']}."
    )

    metadata = {
        "type": "group_info",
        "source": "weekly_group",
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

def create_counselling_chunks(counselling, centre_data):
    """
    Create a text chunk with metadata for a counselling service.
    
    Args:
        counselling (dict): A dictionary containing information about the counselling service.
        centre_data (list): A list of dictionaries containing centre and group data for a service
    Returns:
        dict: A dictionary containing the text chunk and its associated metadata.
    """
    
    text = (
        f"{counselling['name']} counselling service is available at the {centre_data['location']} centre. "
        f"It is available {counselling['availability']}. "
        f"{counselling['description']}."
    )
    
    metadata = {
        "type": "counselling_info",
        "source": "counselling_service",
        "location": centre_data.get('location', []),
        "address": centre_data.get('address', []),
        "email": centre_data.get('email', []),
        "phone": centre_data.get('phone', []),
        "opening_hours": centre_data.get('opening_hours', []),
        "counselling_name": counselling.get('name', []),
        "day": counselling.get('day', []),
        "time": counselling.get('time', [])
    }
    
    return {'text':text ,'metadata': metadata}



