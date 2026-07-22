import easyocr

reader = easyocr.Reader(
    ['en', 'id'],
    gpu=False,
    model_storage_directory="models/easyocr"
)