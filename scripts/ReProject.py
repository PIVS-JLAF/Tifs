import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def reproject_and_compress_rasterio(input_path, output_path, dst_crs='EPSG:4326'):
    with rasterio.open(input_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height,
            'compress': 'lzw'
        })

        with rasterio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                )
    print(f"Reprojected and compressed to: {output_path}")

def reproject_tif_in_folder(parent_folder):
    # Create 'reprojected' folder if it doesn't exist
    reprojected_folder = os.path.join(parent_folder, 'reprojected')
    os.makedirs(reprojected_folder, exist_ok=True)

    # Only get .tif files in the given directory (not subfolders)
    for file in os.listdir(parent_folder):
        input_path = os.path.join(parent_folder, file)
        if os.path.isfile(input_path) and file.lower().endswith('.tif'):
            output_path = os.path.join(reprojected_folder, file)
            reproject_and_compress_rasterio(input_path, output_path)

# Example usage:
file = input("Enter the Directory Folder (Ex. 'C:/Desktop/Parent Folder Name'): ")
parent_folder = rf"{file}"
reproject_tif_in_folder(parent_folder)
