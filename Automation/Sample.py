




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os
import pandas as pd
import openai
from fuzzywuzzy import fuzz
import fitz  # PyMuPDF

# ✅ Load OpenAI API Key
openai.api_key = ""  # Replace with your OpenAI API key

# 📂 Excel file path
excel_file = "whatsapp_chat_sessions.xlsx"

pdf_files = ["./Adiabatic.pdf", "./Cooling.pdf", "./DSS.pdf"] # Replace with actual file paths


# ✅ Define sheet names and associated keywords
SHEET_KEYWORDS = {
    "adiabatic": ["adiabatic", "cooling", "system"],
    "advertisement": ["advertisement", "ad", "promotion"],
    "site visit": ["site visit", "meeting", "appointment"],
    "dust suppression": ["dust suppression", "dust control", "dust"],
    "fog cannon": ["fog cannon", "fogging", "fog", "cannon", "canon"],
    "purchase order": ["purchase order", "po", "order"],
    "misting": ["misting", "mist"],
    "nozzle": ["nozzle", "spray nozzle", "nozzle tip"],
    "support": ["support", "help", "issue", "problem", "order status", "assistance", "query", "question"],
    "others": [],  # Default sheet for unmatched messages
}


# ✅ Function to extract text from multiple PDFs
def extract_text_from_pdfs(pdf_paths):
    all_text = []
    for pdf_path in pdf_paths:
        try:
            doc = fitz.open(pdf_path)
            text = "\n".join(page.get_text() for page in doc)
            all_text.append(text)
        except Exception as e:
            print(f"❌ Error reading {pdf_path}: {e}")

    # ✅ Combine all PDF text but limit it to avoid exceeding token limits
    return "\n\n".join(all_text)[:3000]  # Keeping within token limits


# ✅ Function to get ChatGPT response with multiple PDF contexts
def get_chatgpt_response(query, pdf_paths=[]):
    try:
        pdf_text = extract_text_from_pdfs(pdf_paths) if pdf_paths else ""
        context = f"Relevant PDF content:\n{pdf_text}\n\nUser query: {query}" if pdf_text else query

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": context}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠ Error getting ChatGPT response: {e}")
        return "I'm sorry, I couldn't process your request."

# ✅ Function to check if a conversation should be marked as completed
def is_conversation_completed(message, ai_response):
    """
    Determines if a conversation should be marked as completed based on the message or AI response.
    """
    # Example: Mark as completed if the AI response contains "thank you" or "resolved"
    completion_keywords = ["thank you", "resolved", "completed", "done"]
    for keyword in completion_keywords:
        if keyword in ai_response.lower():
            return True
    return False


# ✅ Function to categorize messages
def determine_target_sheet(body):
    body_lower = body.lower()
    best_match = ("others", 0)  # Default category

    for sheet_name, keywords in SHEET_KEYWORDS.items():
        for keyword in keywords:
            score = fuzz.partial_ratio(keyword.lower(), body_lower)
            if score > best_match[1]:
                best_match = (sheet_name, score)

    # ✅ Force "others" for messages below 60% similarity
    if best_match[1] < 60:
        print(f"⚠ No strong keyword match for '{body}'. Storing in 'others'.")
        return "others"

    print(f"✅ Matched '{body}' to '{best_match[0]}' with {best_match[1]}% confidence.")
    return best_match[0]


# ✅ Function to save messages in categorized Excel sheets
def save_to_excel(chat_name, query, response, conversation_completed=False):
    formatted_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ✅ Load existing data if file exists
    if os.path.exists(excel_file):
        try:
            with pd.ExcelFile(excel_file, engine="openpyxl") as xls:
                sheets = xls.sheet_names
            df_dict = {sheet: pd.read_excel(excel_file, sheet_name=sheet) for sheet in sheets}
        except Exception as e:
            print(f"❌ ERROR: Unable to read Excel file: {e}")
            df_dict = {}
    else:
        df_dict = {}

    # ✅ Search for an existing row with the same chat name & "Under Conversation" status
    existing_row_found = False
    for sheet_name, df in df_dict.items():
        match = df[(df["Chat Name"] == chat_name) & (df["Status"] == "Under Conversation")]

        if not match.empty:
            # ✅ Get the last row index for this chat
            chat_index = match.index[-1]

            # ✅ Find the next available Query & Response columns
            query_cols = [col for col in df.columns if col.startswith("Query")]
            response_cols = [col for col in df.columns if col.startswith("Response")]

            next_query_col = f"Query{len(query_cols) + 1}"
            next_response_col = f"Response{len(response_cols) + 1}"

            # ✅ Add new columns if necessary
            if next_query_col not in df.columns:
                df[next_query_col] = None
            if next_response_col not in df.columns:
                df[next_response_col] = None

            # ✅ Store new query and response in the same row
            df.at[chat_index, next_query_col] = query
            df.at[chat_index, next_response_col] = response

            # ✅ Mark conversation as completed only if explicitly flagged
            if conversation_completed:
                df.at[chat_index, "Status"] = "Completed"
                print(f"✅ Updated status to 'Completed' for chat '{chat_name}'")
            else:
                df.at[chat_index, "Status"] = "Under Conversation"

            # ✅ Update sheet data
            df_dict[sheet_name] = df
            existing_row_found = True
            break  # Stop searching after finding a match

    if not existing_row_found:
        # ✅ If no existing "Under Conversation" row is found, determine the target sheet using keywords
        target_sheet = determine_target_sheet(query)

        # ✅ Ensure the sheet exists
        if target_sheet not in df_dict:
            df_dict[target_sheet] = pd.DataFrame(columns=["Status", "Date/Time", "Chat Name", "Query", "Response"])

        df = df_dict[target_sheet]

        # ✅ Insert new row in the correct sheet
        new_row = {
            "Date/Time": formatted_time,
            "Chat Name": chat_name,
            "Query": query,
            "Response": response,
            "Status": "Under Conversation"  # Default status for new rows
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df_dict[target_sheet] = df

    # ✅ Save everything back to Excel
    try:
        with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
            for sheet, df in df_dict.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        print(f"✅ Data saved in '{excel_file}'.")
    except Exception as e:
        print(f"❌ ERROR: Failed to save data to Excel: {e}")

# ✅ Set up Chrome WebDriver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=" + os.path.join(os.getcwd(), "whatsapp_session"))
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("detach", True)

# ✅ Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # ✅ Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    print("Waiting for WhatsApp Web to load...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
    )
    print("✅ Logged in successfully!")

    # Trigger the Unread Tab if available
    try:
        unread_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "unread-filter"))
        )
        unread_button.click()
        print("✅ Clicked on the 'Unread' tab successfully!")
    except Exception as e:
        print(f"⚠ Error clicking on 'Unread' tab: {e}")

    while True:
        try:
            # 🔍 Detect unread messages in the chat list
            unread_chats = driver.find_elements(By.XPATH, '//span[contains(@aria-label, "unread message")]')
            if unread_chats:
                print(f"🔔 Found {len(unread_chats)} unread messages.")

                for chat in unread_chats:
                    try:
                        chat.click()
                        time.sleep(2)

                        # 🔍 Get chat name from header
                        chat_name = driver.find_element(By.XPATH, '//header//span[@dir="auto"]').text.strip()

                        # 🔍 Try to extract the unread count (e.g., "2 unread messages")
                        try:
                            unread_count_elem = driver.find_element(By.XPATH,
                                                                    '//span[contains(@class, "x9f619") and contains(text(), "unread message")]'
                                                                    )
                            unread_text = unread_count_elem.text
                            unread_count = int(unread_text.split()[0])
                        except Exception as e:
                            print(f"⚠ Unread count not found, defaulting to 1: {e}")
                            unread_count = 1  # default to 1 if unread count not found

                        # 🔄 Get all message text elements in the chat (using "copyable-text")
                        all_messages = driver.find_elements(By.XPATH,
                                                            '//div[contains(@class, "message-in")]//div[@class="copyable-text"]'
                                                            )

                        if all_messages:
                            # Ensure we don't try to get more messages than available
                            unread_count = min(unread_count, len(all_messages))
                            # Select the last N unread messages
                            unread_messages = [msg.text.strip() for msg in all_messages[-unread_count:]]

                            # Process each message individually
                            for i, message in enumerate(unread_messages):
                                print(f"📩 Unread message {i + 1} from {chat_name}:\n{message}")

                                # ✅ Send the message to ChatGPT
                                ai_response = get_chatgpt_response(message)
                                print(f"🤖 AI Response: {ai_response}")

                                # ✅ Check if the conversation should be marked as completed
                                conversation_completed = is_conversation_completed(message, ai_response)

                                # ✅ Save conversation to Excel
                                save_to_excel(chat_name, message, ai_response, conversation_completed)
                        else:
                            print(f"⚠ No messages found in chat {chat_name}.")

                        # 🔙 Close the chat.
                        # First, try to click the back button if available.
                        try:
                            back_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Back"]'))
                            )
                            back_button.click()
                            print(f"🔴 Closed chat with {chat_name} using back button.")
                        except Exception as e:
                            print(f"⚠ Error clicking back button: {e}. Using ESCAPE key as fallback.")
                            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                        # Optional: wait a few seconds after closing the chat before continuing
                        time.sleep(5)

                    except Exception as e:
                        print(f"⚠ Error processing chat: {e}")

            else:
                print("🔍 No unread messages found. Waiting...")

            # 🔄 Wait before checking again
            time.sleep(5)

        except Exception as e:
            print(f"⚠ Unexpected error: {e}")

except Exception as e:
    print(f"❌ Critical Error: {e}")

finally:
    print("🔴 Script running. Press CTRL+C to stop manually.")