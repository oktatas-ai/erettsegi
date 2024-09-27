from PIL import Image


def are_images_adjacent(img1, img2, tolerance=1):
    pos1, pos2 = img1["position"], img2["position"]

    if img1["extension"] != img2["extension"]:
        return False

    horizontal = (
        abs(pos1["x"] + pos1["w"] - pos2["x"]) < tolerance
        or abs(pos2["x"] + pos2["w"] - pos1["x"]) < tolerance
    )

    vertical = (
        abs(pos1["y"] + pos1["h"] - pos2["y"]) < tolerance
        or abs(pos2["y"] + pos2["h"] - pos1["y"]) < tolerance
    )

    return (horizontal and abs(pos1["y"] - pos2["y"]) < tolerance) or (
        vertical and abs(pos1["x"] - pos2["x"]) < tolerance
    )


def merge_images(img1, img2):
    pos1, pos2 = img1["position"], img2["position"]

    x = min(pos1["x"], pos2["x"])
    y = min(pos1["y"], pos2["y"])
    w = max(pos1["x"] + pos1["w"], pos2["x"] + pos2["w"]) - x
    h = max(pos1["y"] + pos1["h"], pos2["y"] + pos2["h"]) - y

    merged_image = Image.new("RGB", (int(w), int(h)), (255, 255, 255))

    for img in [img1, img2]:
        pos = img["position"]
        img_resized = img["image"].resize((int(pos["w"]), int(pos["h"])))
        merged_image.paste(img_resized, (int((pos["x"] - x)), int((pos["y"] - y))))

    return {
        "page": img1["page"],
        "index": f"{img1['index']}-{img2['index']}",
        "image": merged_image,
        "extension": img1["extension"],
        "position": {"x": x, "y": y, "w": w, "h": h},
    }


def merge_adjacent_images(images):
    merged = True
    while merged:
        merged = False
        for i in range(len(images)):
            for j in range(i + 1, len(images)):
                if images[i]["page"] == images[j]["page"] and are_images_adjacent(
                    images[i], images[j]
                ):
                    merged_image = merge_images(images[i], images[j])
                    images = [
                        img for k, img in enumerate(images) if k not in [i, j]
                    ] + [merged_image]
                    merged = True
                    break
            if merged:
                break
    return images
