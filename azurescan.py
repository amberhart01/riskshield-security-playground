from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def scan_a81_user_endpoint_protection(subscription_id):
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    
    results = []

    for vm in compute_client.virtual_machines.list_all():
        rg = vm.id.split("/")[4]
        instance_view = compute_client.virtual_machines.instance_view(rg, vm.name)
        
        # Check for antimalware extension
        has_antimalware = any(
            ext.name.lower() == "iisantimalware" or "antimalware" in ext.name.lower()
            for ext in vm.resources if hasattr(vm, 'resources')
        )

        # Check if disks are encrypted
        os_disk_encrypted = vm.storage_profile.os_disk.encryption_settings is not None

        results.append({
            "resource": vm.name,
            "resource_group": rg,
            "location": vm.location,
            "has_antimalware": has_antimalware,
            "disk_encrypted": os_disk_encrypted,
            "control_id": "A.8.1",
            "status": "pass" if has_antimalware and os_disk_encrypted else "fail",
            "notes": f"{'✔' if has_antimalware else '✘'} Antimalware, {'✔' if os_disk_encrypted else '✘'} Encryption"
        })

    return results
