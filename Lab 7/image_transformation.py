from PIL import Image
import numpy as np

# Read image
img = Image.open("image.jpg").resize((32, 32))
img_array = np.array(img)

# Save to text file
np.savetxt("pixels.txt", img_array.reshape(-1, 3), fmt='%d')

# Load and reconstruct
loaded = np.loadtxt("pixels.txt", dtype=np.uint8).reshape(32, 32, 3)
Image.fromarray(loaded).save("reconstructed.jpg")

print("Conversion successful!")

## Alternative 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# Step 1: Read the JPG image
img = Image.open(r"C:\Users\Student\Downloads\images_test.jpg")
img = img.resize((32, 32)) 
img_array = np.array(img)

# Step 2: Save pixel data to text file
np.savetxt("test.txt", img_array.reshape(-1, img_array.shape[2]), fmt='%d')
print("Image converted to text and saved as any.txt")

# Step 3: Read the text file back and reshape it
loaded_array = np.loadtxt("test.txt", dtype=np.uint8)
loaded_array = loaded_array.reshape(img_array.shape)

# Step 4: Convert array back to image
new_img = Image.fromarray(loaded_array)
new_img.save("new.jpg")
print("Text file reconverted to new.jpg")

# Step 5: Display both images side by side for comparison
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].imshow(img)
axes[0].set_title("Original Image")
axes[0].axis("off")

axes[1].imshow(new_img)
axes[1].set_title("Reconstructed Image")
axes[1].axis("off")