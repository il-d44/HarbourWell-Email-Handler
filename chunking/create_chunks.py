import json

def create_chunks(centre_data):
    chunks = []

    # Centre-level info
    intro = (
        f"{centre_data['service_name']} is located at {centre_data['address']}. "
        f"It is open {centre_data['opening_hours']}. Services offered include: "
        f"{', '.join(centre_data['services'])}."
    )
    chunks.append(intro)

    contact = (
        f"You can contact the {centre_data['service_name']} by calling {centre_data['phone']} "
        f"or emailing {centre_data['email']}."
    )
    chunks.append(contact)

    # Function to chunk a detailed group
    def chunk_detailed_group(group, service_name):
        detailed_chunks = []

        core = (
            f"The '{group['name']}' runs at the {service_name} centre on {group['day']}s at {group['time']}."
        )
        if 'duration' in group:
            core += f" It runs for {group['duration']}."
        if group.get('registration_required'):
            core += " Registration is required."
        detailed_chunks.append(core)

        if 'description' in group:
            detailed_chunks.append(f"About the group: {group['description']}")

        if 'topics' in group and group['topics']:
            topic_text = "Topics covered include: " + "; ".join(group['topics']) + "."
            detailed_chunks.append(topic_text)

        if 'who_is_it_for' in group:
            detailed_chunks.append(f"This group is suitable for: {group['who_is_it_for']}")

        return detailed_chunks

    # Group info (both basic and detailed)
    for group in centre_data.get("weekly_groups", []):
        # Detailed group if has extended info
        if any(k in group for k in ['topics', 'description', 'who_is_it_for']):
            detailed_chunks = chunk_detailed_group(group, centre_data["service_name"])
            chunks.extend(detailed_chunks)
        
        # Simpler group fallback
        group_name = group["name"]
        day = group["day"]
        time = group["time"]

        if day == "TBC" or "on hold" in time.lower():
            group_chunk = (
                f"The {group_name} at {centre_data['service_name']}  is currently on hold. "
                f"It is expected to return later, likely in the spring."
            )
        else:
            group_chunk = (
                f"The {group['name']} meets at the {centre_data['service_name']} every {group['day']} from {group['time']}."
            )
            if "link" in group:
                group_chunk += f" Find out more here: {group['link']}"
        chunks.append(group_chunk)
    return chunks

# Load your JSON data (replace this with your actual JSON loading method)
with open("service_data/services.json", "r") as f:
    service_data = json.load(f)

# Generate chunks

service_chunks = [create_chunks(service) for service in service_data]

print(service_chunks)


# for service in service_data:
#     for group in service.get("weekly_groups", []):
#         print("Checking group:", group)  # Debug print