import face_recognition
import cv2
import pickle

# Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

# Print available keys in the pickle
print("[INFO] Keys in the encodings file:", list(data.keys()))

# Try to find appropriate keys
if "encodings" in data and "names" in data:
    known_face_encodings = data["encodings"]
    known_face_names = data["names"]
elif "face_encodings" in data and "face_names" in data:
    known_face_encodings = data["face_encodings"]
    known_face_names = data["face_names"]
else:
    # Pick the first two keys as a fallback
    keys = list(data.keys())
    known_face_encodings = data[keys[0]]
    known_face_names = data[keys[1]]

# Initialize webcam
video_capture = cv2.VideoCapture(0)

print("[INFO] Starting camera. Press 'q' to quit.")
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("[ERROR] Failed to grab frame from camera.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, encoding)
        name = "Unknown"

        # Use the known face with the smallest distance if there are matches
        face_distances = face_recognition.face_distance(known_face_encodings, encoding)
        if len(face_distances) > 0:
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        face_names.append(name)

    # Display results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
