import face_recognition
import os
import pickle

# Path to your dataset
dataset_dir = "dataset"

# Lists to hold encodings and names
encodings = []
names = []

print("[INFO] Processing dataset...")

# Loop over each person in the dataset
for person_name in os.listdir(dataset_dir):
    person_folder = os.path.join(dataset_dir, person_name)
    if not os.path.isdir(person_folder):
        continue

    print(f"[INFO] Encoding faces for {person_name}...")
    
    # Loop over images of the person
    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        
        try:
            image = face_recognition.load_image_file(image_path)
            face_encs = face_recognition.face_encodings(image)
            
            if len(face_encs) > 0:
                encodings.append(face_encs[0])
                names.append(person_name)
            else:
                print(f"[WARNING] No face found in {image_path}")
        except Exception as e:
            print(f"[ERROR] Could not process {image_path}: {e}")

# Save the encodings to a pickle file
data = {"encodings": encodings, "names": names}
with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("[INFO] Encodings saved to encodings.pkl")
