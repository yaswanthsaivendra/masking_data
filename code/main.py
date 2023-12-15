import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import glob
from utils import mask_private_info
import os
from tqdm import tqdm
import tkinter as tk
from gui import SimpleGUI



parent_dir = os.path.abspath(os.pardir)
gui = None


## Model Import
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-ner-cased")
model = AutoModelForTokenClassification.from_pretrained("savasy/bert-base-turkish-ner-cased")
ner=pipeline('ner', model=model, tokenizer=tokenizer)



def start_masking_func():
  try:
    data_col = "Verbatim"
    #read all files in input_files
    files = glob.glob(os.path.join("C:\\Windows\\tmp\\*"))
    if len(files) == 0:
      log_text = "0 files found please add your csv files under input_files directory\n"
      print(log_text)
      gui.logs_text.insert(tk.END, log_text)
      return log_text

    log_text = f"{len(files)} found files in input files\n"

    print(log_text)
    gui.logs_text.insert(tk.END, log_text)


    for file in files:
      ## read file
      if "/" in file:
        filename = file.split("/")[-1]
      else:
        filename = file.split("\\")[-1]

      log_text = f"reading file {filename} started\n"
      print(log_text)
      gui.logs_text.insert(tk.END, log_text)
      if ".csv" in filename:
          #read file
          try:
            df = pd.read_csv(file)
            read_csv_success = True
          except Exception as e:
            read_csv_success = False
          if read_csv_success is False:
            #read csv in a diffrent turkish supporting encoding
            tr_char_encoding = ["cp1026", "iso8859_9", "mac_turkish", "cp857", "cp1254", "cp857"]
            reading_encoding = False
            for encoding in tr_char_encoding:
              try:
                gui.logs_text.insert(tk.END, f"encoding with {encoding} started\n")
                df = pd.read_csv(file, encoding=encoding)
                gui.logs_text.insert(tk.END, f"encoding with {encoding} succeeded\n")
                reading_encoding = True
                break
              except Exception as e:
                gui.logs_text.insert(tk.END, f"encoding with {encoding} failed\n")


            if reading_encoding is False:
              print(f"Unable to read this file {filename}, your file structure might be corrupt")
              gui.logs_text.insert(tk.END, f"Unable to read this file {filename}, your file structure might be corrupt\n")
              continue
      elif ".xlsx" in filename:
        try:
            df = pd.read_excel(file, engine="openpyxl")
        except Exception as e:
            gui.logs_text.insert(tk.END, f"reading excel file {filename} failed\n")
            continue
            
      else:
        print("Your files should be in csv : comma seperated format")
        continue
      print("we are out of reading")
      if data_col not in df.columns:
        print("Data column not found")
        return "Data column not found"


      print(f"Processing {len(df)} lines in the file {filename} started....")
      gui.logs_text.insert(tk.END, f"Processing {len(df)} lines in the file {filename} started....\n")
      
      new_texts = []
      ## Mask User info Section   
      masked_lines_counter = 0
      processed_lines = 0
      texts = df[data_col].values.tolist()
      for text_index in tqdm(range(len(df))):
        #process text
        masked_text = mask_private_info(texts[text_index],ner)
        new_texts.append(str(masked_text))
        #check if any info was masked
        
        if "*****" in str(masked_text):
          masked_lines_counter += 1
        # processed_lines += 1
        # if processed_lines % 10 == 0:
          # print(f"{masked_lines_counter}/{processed_lines} were masked")
          # logger.info(f"{masked_lines_counter}/{processed_lines} were masked")

      df["Masked"] = new_texts
      #drop original column
      df = df.drop([data_col],axis=1)
      #save new file
      if ".csv" in filename:
        df.to_csv(os.path.join("C:\\Windows\\tmp\\"+filename),index=False,encoding="utf-8-sig")
      else:
        df.to_excel(os.path.join("C:\\Windows\\tmp\\"+filename),index=False)
      
      log_text = f"Checking {filename} finished with {masked_lines_counter}/{processed_lines} lines masked\n"

      print(log_text)
      gui.logs_text.insert(tk.END, log_text)
    gui.logs_text.see(tk.END) 

  except Exception as e:
    print(f"Main function failed with error {e}")
    gui.logs_text.insert(tk.END, f"Main function failed with error {e}\n")
    gui.logs_text.see(tk.END) 
    return e


def main():
  root = tk.Tk()
  global gui
  gui = SimpleGUI(root, start_masking_func)
  root.mainloop()


main()