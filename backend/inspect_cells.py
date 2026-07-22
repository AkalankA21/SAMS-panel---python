from app.sams import SAMS

sams = SAMS('data/images/5.jpeg', 'data/resources/students.xml')
image_data = sams.run()
print(f"Warped Image Dimensions: {image_data.perspective_image.shape if image_data.perspective_image is not None else None}")
for c in image_data.cells:
    print(f"Cell ID {c['id']}: Row {c['row']}, Col {c['column']}, Bbox {c['bbox']}")
