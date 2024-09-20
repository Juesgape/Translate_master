import pandas as pd
import time
from src.translate_content import translate_content

def process_translation(file_path, output_path, is_title = False):
    #Reading csv file
    data_to_translate = pd.read_csv(file_path)

    #Propmt text
    custom_prompt = ""

    filter_data_descriptions = (
        (data_to_translate["Field"] == "body_html") |
        (data_to_translate["Field"] == "meta_description")
    )

    #Filtering data so that we get the columns that we want to, in the future, work with them
    descriptions_info = data_to_translate[filter_data_descriptions][["Identification", "Field", "Default content"]]
    #Converting to data frame to a dictionary
    descriptions_list = descriptions_info.to_dict(orient="records")

    #We will save all of our translations here
    translated_descriptions = []
    
    #This will help us controle the while loop
    descriptions_count = 0
    descriptions_len = len(descriptions_list)
    descriptions_increment = 100 if is_title == True else 10

    while descriptions_count < descriptions_len:
        #Getting only 10 descriptions
        batch = descriptions_list[descriptions_count : descriptions_count + descriptions_increment]
        data_to_send = [item['Default content'] for item in batch]
        identifications_to_send = [item['Identification'] for item in batch]

        try:
            translated_data = translate_content(data_to_send, is_title)

            if translated_data:
                for i, translated_text in enumerate(translated_data):
                    translated_descriptions.append({
                        'Identification': identifications_to_send[i],
                        'Field': batch[i]['Field'],
                        'Translated content': translated_text
                    })

            descriptions_count += descriptions_increment
            print(f'{descriptions_count} elements processed...')
            time.sleep(20)

        except Exception as e:
            print(f"Error at {descriptions_count}: {e}")
            descriptions_count += descriptions_increment

    translated_df = pd.DataFrame(translated_descriptions)
    translated_df.to_excel(output_path, index=False)
    print(f"File saved at {output_path}")
