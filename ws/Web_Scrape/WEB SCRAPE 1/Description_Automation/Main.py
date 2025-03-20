import pandas as pd
import openai
import time

# Set your OpenAI API key
openai.api_key = "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"

# Function to generate a product description
def generate_description(product_title):
    try:
        # Create a chat-based API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a short, creative and engaging description between 50-100 words for the following title: '{product_title}'."}
            ]
        )
        return response.choices[0].message['content'].strip()

    except Exception as e:
        print(f"Error generating description for '{product_title}': {e}")
        raise e


# Main function to process the Excel file
def process_excel(file_path):
    try:
        df = pd.read_excel(file_path)

        if 'TITLE' not in df.columns:
            raise ValueError("The column 'TITLE' does not exist in the Excel file.")

        if 'DESCRIPTION' not in df.columns:
            df['DESCRIPTION'] = ""

        generation_count = 0

        for index, row in df.iterrows():
            title = row['TITLE']
            description = row['DESCRIPTION']

            if pd.isna(title) or title.strip() == "":
                print(f"Skipping empty title at row {index + 2}.")

                if index == len(df) - 1:
                    print("Last row is empty. Terminating process.")
                    break
                continue

            if pd.isna(description) or description.strip() == "":
                try:
                    generation_count += 1
                    print(f"<<{ generation_count }>> Generating description for: {title}")
                    description = generate_description(title)
                    df.at[index, 'DESCRIPTION'] = description

                    print(f"Success: Description for '{title}' generated and stored.")

                    df.to_excel(file_path, index=False)
                    print("Excel file updated successfully...!!!")
                    print("<=================================================================================================>")

                    print("Cooldown few seconds before the next API call...!!!")
                    time.sleep(3)

                except Exception as e:
                    print(f"Failure: Could not generate description for '{title}'. Stopping process.")
                    break

            else:
                print(f"Description already exists for '{title}', skipping description generation.")

        print(f"Total descriptions generated: {generation_count}")

    except Exception as e:
        print(f"Error processing Excel file: {e}")


# Main execution
if __name__ == "__main__":
    # Pass excel file with title and empty description column here
    excel_file_path = "Output.xlsx"
    process_excel(excel_file_path)