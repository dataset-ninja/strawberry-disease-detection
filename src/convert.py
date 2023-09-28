import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_ext
from supervisely.io.json import load_json_file

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    train_path = os.path.join("Strawberry Disease","train")
    val_path = os.path.join("Strawberry Disease","val")
    test_path_1 = os.path.join("Strawberry Disease","Test Disease Severity Level","Level 1")
    test_path_2 = test_path_1 = os.path.join("Strawberry Disease","Test Disease Severity Level","Level 2")
    batch_size = 30
    ds_name = "ds"
    images_ext = ".jpg"
    anns_ext = ".json"

    ds_to_path = {"train": train_path, "val": val_path, "test": test_path_1, "test_2": test_path_2}


    def create_ann(image_path):
        labels = []
        tags = []

        tag_meta = ds_to_tag.get(ds_name)
        if tag_meta is not None:
            tag = sly.Tag(tag_meta)
            tags.append(tag)

        image_name = get_file_name(image_path)
        ann_path = os.path.join(data_path, image_name + anns_ext)
        ann_data = load_json_file(ann_path)
        img_height = ann_data["imageHeight"]
        img_wight = ann_data["imageWidth"]

        for curr_poly in ann_data["shapes"]:
            class_name = curr_poly["label"]
            obj_class = meta.get_obj_class(class_name)
            polygons_coords = curr_poly["points"]
            exterior = []
            for coords in polygons_coords:
                exterior.append([int(coords[1]), int(coords[0])])
            poligon = sly.Polygon(exterior)
            label_poly = sly.Label(poligon, obj_class)
            labels.append(label_poly)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)


    powdery_mildew_leaf = sly.ObjClass("Powdery Mildew Leaf", sly.Polygon)
    anthracnose = sly.ObjClass("Anthracnose Fruit Rot", sly.Polygon)
    fruit = sly.ObjClass("Powdery Mildew Fruit", sly.Polygon)
    leaf_spot = sly.ObjClass("Leaf Spot", sly.Polygon)
    angular = sly.ObjClass("Angular Leafspot", sly.Polygon)
    blossom = sly.ObjClass("Blossom Blight", sly.Polygon)
    mold = sly.ObjClass("Gray Mold", sly.Polygon)

    tag_label_1 = sly.TagMeta("label 1", sly.TagValueType.NONE)
    tag_label_2 = sly.TagMeta("label 2", sly.TagValueType.NONE)
    ds_to_tag = {"test": tag_label_1, "test_2": tag_label_2}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[powdery_mildew_leaf, anthracnose, fruit, leaf_spot, angular, blossom, mold],
        tag_metas=[tag_label_1, tag_label_2],
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, data_path in ds_to_path.items():
        if ds_name != "test_2":
            dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_names = [
            im_name for im_name in os.listdir(data_path) if get_file_ext(im_name) == images_ext
        ]

        progress = sly.Progress("Add data to {} dataset".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(data_path, image_name) for image_name in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))
    
    return project
