import json
import google.generativeai as genai
import streamlit as st

class PrescriptionParser:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_json_from_response(self, response_text):
        try:
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            if "'" in json_str and '"' not in json_str:
                json_str = json_str.replace("'", '"')
            result = json.loads(json_str)
            # Ensure all expected fields present, add default if missing
            keys = ["patient_name", "date", "address", "doctor_name", "diagnosis",
                    "history_symptoms", "remarks", "medications", "refill"]
            for key in keys:
                if key not in result:
                    result[key] = "N/A" if key != "medications" else []
            return result
        except Exception as e:
            st.error(f"Failed to parse JSON response: {str(e)}")
            st.code(response_text, language="text")
            return None

    def parse_prescription(self, enhanced_image, status_placeholder=None):
        prompt = """
        Extract the following information from this medical prescription image with maximum precision:

        1. Patient name (first and last name)
        2. Date (format as MM/DD/YY)
        3. Address (city, state if visible)
        4. Doctor's name
        5. Diagnosis
        6. History or Symptoms
        7. Medications with dosage, frequency, and duration
        8. Refill information
        9. Remarks or additional notes if present

        Important notes:
        - Maintain original spelling
        - Return JSON only in this format:

        {
          "patient_name": "Full Name",
          "date": "MM/DD/YY",
          "address": "Complete address as shown",
          "doctor_name": "Doctor's Full Name",
          "diagnosis": "Diagnosis details",
          "history_symptoms": "History or symptoms noted",
          "medications": [
            {
              "name": "Medication name",
              "dosage": "Dosage amount",
              "frequency": "Directions for use",
              "duration": "Duration if specified"
            }
          ],
          "refill": "Refill information if present",
          "remarks": "Additional remarks or notes"
        }
        """
        try:
            if status_placeholder:
                status_placeholder.info("Sending enhanced image for analysis...")
            response = self.model.generate_content([prompt, enhanced_image])
            result = self.extract_json_from_response(response.text)
            if status_placeholder:
                status_placeholder.empty()
            return result
        except Exception as e:
            st.error(f"Error analyzing prescription: {str(e)}")
            return None
