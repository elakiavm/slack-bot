'''
Created on

Course work:

@author: TactBOT 2.0 Team

Source:

'''

# Import necessary modules
import pandas as pd
import random



def check_if_comedy(text):

    comedians_url = "static/tact-bot-2.0 - Comedians.csv"
    comedy_df=pd.read_csv(comedians_url)
    comedians_list=comedy_df.Comedian.to_list()
    # print(comedians_list)

    sitcoms_url = "static/tact-bot-2.0 - Sitcoms.csv"
    sitcom_df=pd.read_csv(sitcoms_url)
    sitcoms_list=sitcom_df['TV Show Name'].to_list()
    # print(sitcoms_list)

    text = text.lower()
    # print(text)

    if text in comedians_list or text in sitcoms_list:

        return True

    return False

def execute_comedy(text):

    comedians_url = "static/tact-bot-2.0 - Comedians.csv"
    comedy_df=pd.read_csv(comedians_url)
    comedians_list=comedy_df.Comedian.to_list()
    # print(comedians_list)

    sitcoms_url = "static/tact-bot-2.0 - Sitcoms.csv"
    sitcom_df=pd.read_csv(sitcoms_url)
    sitcoms_list=sitcom_df['TV Show Name'].to_list()
    # print(sitcoms_list)

    text = text.lower()
    
    if text in comedians_list:
        
        df = comedy_df[comedy_df.Comedian == text]

        required_list = df.Punchline.to_list()

        punchline = random.choice(required_list)

        # print(punchline)

    if text in sitcoms_list:
        
        df = sitcom_df[sitcom_df['TV Show Name'] == text]
        
        required_list = df.Punchline.to_list()

        punchline = random.choice(required_list)

        # print(punchline)

    return punchline

def startpy():

    text="VaDivEl"

    check_if_comedy(text)

    execute_comedy(text)


if __name__ == '__main__':
    
    startpy()


    
