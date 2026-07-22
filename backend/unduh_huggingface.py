from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Salesforce/blip-image-captioning-base",
    local_dir="backend/models/blip"
)