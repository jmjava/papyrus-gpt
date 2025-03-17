import xml.etree.ElementTree as ET

def get_namespaces(xmi_file):
    """Extract XML namespaces from the XMI file."""
    events = "start", "start-ns"
    ns_map = {}
    for event, elem in ET.iterparse(xmi_file, events):
        if event == "start-ns":
            ns_map[elem[0]] = elem[1]
    return ns_map

def load_xmi(xmi_file):
    """Load an XMI file and return its parsed XML root and namespaces."""
    tree = ET.parse(xmi_file)
    root = tree.getroot()
    namespaces = get_namespaces(xmi_file)
    return root, namespaces

def extract_classes(model_xmi):
    """Extract UML class names and their IDs from the model XMI file."""
    model_root, namespaces = load_xmi(model_xmi)
    classes = {}

    # Find all UML classes
    # for uml_class in model_root.findall(".//uml:packagedElement", namespaces):
    #     if uml_class.get(f"{{{namespaces['xmi']}}}type") == "uml:Class":
    #         class_id = uml_class.get(f"{{{namespaces['xmi']}}}id")
    #         class_name = uml_class.get("name")  # Extract the class name directly

    #         if class_id and class_name:
    #             classes[class_id] = class_name  # Correctly store the mapping

    # print("\n✅ DEBUG: Extracted UML Classes")
    # for cid, cname in classes.items():
    #     print(f"  {cid} -> {cname}")

    # Find all UML classes
    for uml_class in model_root.findall(".//packagedElement"):
        if uml_class.get(f"{{{namespaces['xmi']}}}type") == "uml:Class":
            class_id = uml_class.get(f"{{{namespaces['xmi']}}}id")
            class_name = uml_class.get("name")  # Extract the class name directly

            if class_id and class_name:
                classes[class_id] = class_name  # Correctly store the mapping

    print("\n✅ DEBUG: Extracted UML Classes")
    for cid, cname in classes.items():
        print(f"  {cid} -> {cname}")

    return classes


def extract_applied_stereotypes(model_xmi, classes):
    """Extract applied stereotypes and link them to the correct class names."""
    model_root, namespaces = load_xmi(model_xmi)
    applied_stereotypes = []

    # Find elements that apply stereotypes via base_Class
    for element in model_root.iter():
        if "base_Class" in element.attrib:
            stereotype_name = element.tag.split("}")[-1]  # Extract stereotype name
            base_class_id = element.get("base_Class")  # Get the class ID it applies to

            # Use the correct name instead of "Unknown Class"
            class_name = classes.get(base_class_id, "UNKNOWN")
            applied_stereotypes.append((class_name, base_class_id, stereotype_name))

    return applied_stereotypes

def main(profile_xmi_path, model_xmi_path):
    """Extract and display UML class stereotypes."""
    # Extract class names from the model
    classes = extract_classes(model_xmi_path)

    # Extract applied stereotypes and ensure correct class name mapping
    applied_stereotypes = extract_applied_stereotypes(model_xmi_path, classes)

    # Print results
    print("\nApplied Stereotypes:")
    print(f"{'Class Name':<20} {'Class ID':<40} {'Applied Stereotype'}")
    print("-" * 80)
    for class_name, class_id, stereotype in applied_stereotypes:
        print(f"{class_name:<20} {class_id:<40} {stereotype}")

if __name__ == "__main__":
    # Set file paths
    profile_xmi_path = "/home/ubuntu/Documents/github/papyrus-gpt/src/chatmodel.profile.uml"  # Not needed for this case, kept for structure
    model_xmi_path = "/home/ubuntu/Documents/github/papyrus-gpt/src/model.uml"

    # Run the script
    main(profile_xmi_path, model_xmi_path)