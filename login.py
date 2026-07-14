# login.py
from playwright.sync_api import sync_playwright

def start_login():
    with sync_playwright() as p:
        # 'user_data' అనే ఫోల్డర్ లో మీ లాగిన్ డేటా మొత్తం సేవ్ అవుతుంది
        user_data_dir = "./user_data"
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel='msedge',
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        )
        
        page = context.pages[0] # Persistent context లో మొదటి పేజీని తీసుకోవాలి
        page.goto("https://gemini.google.com/")
        
        print("\n--- లాగిన్ సెటప్ ---")
        print("బ్రౌజర్ ఓపెన్ అయ్యింది. మీ అకౌంట్ తో లాగిన్ అవ్వండి.")
        input("లాగిన్ పూర్తయ్యాక, ఈ టెర్మినల్ లో Enter నొక్కండి...")
        
        # ఇక్కడ సెషన్ ఫైల్ సేవ్ చేయాల్సిన అవసరం లేదు, 
        # ఎందుకంటే 'user_data' ఫోల్డర్ లో డేటా ఆటోమేటిక్ గా సేవ్ అవుతుంది.
        print("సెషన్ 'user_data' ఫోల్డర్‌లో సేవ్ అయ్యింది.")
        context.close()

if __name__ == "__main__":
    start_login()