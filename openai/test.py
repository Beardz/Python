import os
import openai
from dotenv import load_dotenv

load_dotenv('D:\code\python\openai\apikey.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    pass

if __name__ == "__main__":
    main()
