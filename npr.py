import cv2
import pytesseract
import datetime
import csv

# Constantsz
COOLDOWN_DURATION = datetime.timedelta(minutes=0.4)  # Cooldown duration 

# Initialize variables
last_detection_time = datetime.datetime.min
correct_detection = False

def recognize_plate(plate_img):
    # Pre-process plate image to enhance contrast and remove noise
    plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    plate_img = cv2.GaussianBlur(plate_img, (3, 3), 0)
    plate_img = cv2.threshold(plate_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Apply OCR on plate ROI
    text = pytesseract.image_to_string(plate_img, config='--psm 7')
    return text.strip()

cap = cv2.VideoCapture(0)

# Load the plate detection cascade
plate_cascade = cv2.CascadeClassifier("C:/Users/ashli/OneDrive/Desktop/project/project final/indian_license_plate.xml")

# Open CSV file for writing
with open('number.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Plate Number', 'Date', 'Time']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect plates in the grayscale image
            plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            # Process detected plates
            for (x, y, w, h) in plates:
                roi_gray = gray[y:y + h, x:x + w]
                plate = frame[y:y + h, x:x + w]
                plate_number = recognize_plate(plate)
                if plate_number and len(plate_number) >= 3:
                    current_datetime = datetime.datetime.now()
                    time_since_last_detection = current_datetime - last_detection_time
                    if time_since_last_detection >= COOLDOWN_DURATION and not correct_detection:
                        current_date = current_datetime.strftime('%Y-%m-%d')
                        current_time = current_datetime.strftime('%H:%M:%S')
                        output_str = f"{plate_number} - {current_date} {current_time}"
                        print(output_str)
                        writer.writerow({'Plate Number': plate_number, 'Date': current_date, 'Time': current_time})
                        last_detection_time = current_datetime
                        correct_detection = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, plate_number, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Reset correct_detection flag if no plates detected
            if len(plates) == 0:
                correct_detection = False

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Failed to capture frame.")
            break

# When everything is done, release the capture and close the CSV file
cap.release()
cv2.destroyAllWindows()
csv_file.close()
