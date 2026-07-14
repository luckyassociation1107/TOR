import os
import time
from playwright.sync_api import sync_playwright
from stem import Signal
from stem.control import Controller

input_folder = r"C:\Users\owner\google\iamge generation\downloaded_images"
output_folder = r"C:\Users\owner\google\iamge generation\processed_images"

def renew_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            time.sleep(2)
    except: pass

def run_automation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        while True:
            image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            if not image_files: break
            
            renew_tor_ip()
            context = browser.new_context(proxy={"server": "socks5://127.0.0.1:9050"})
            page = context.new_page()
            
            try:
                page.goto("https://dewatermark.ai/")
                # 'Auto Remove 4.0' క్లిక్
                page.wait_for_selector("text=Auto Remove 4.0")
                page.click("text=Auto Remove 4.0")
                
                for img_name in image_files[:3]:
                    img_path = os.path.join(input_folder, img_name)
                    
                    # అప్‌లోడ్ టెక్నిక్ మారుస్తున్నాను (JavaScript ద్వారా)
                    # ఇది ఫైల్ ఇన్‌పుట్‌ని వెతికి ఫోటో అప్‌లోడ్ చేస్తుంది
                    file_input = page.query_selector("input[type='file']")
                    if file_input:
                        file_input.set_input_files(img_path)
                    else:
                        print("Upload input not found!")
                        break

                    # డౌన్‌లోడ్ బటన్ కోసం వెయిట్
                    # ఇక్కడ బటన్ పైన ఉన్న SVG/Icons కి అడ్డం లేకుండా చూద్దాం
                    print("Waiting for download button...")
                    page.wait_for_function("""
                        () => {
                            const btns = Array.from(document.querySelectorAll('button'));
                            const downloadBtn = btns.find(b => b.innerText.toLowerCase().includes('download'));
                            return downloadBtn && !downloadBtn.disabled;
                        }
                    """, timeout=300000)

                    # డౌన్‌లోడ్ క్లిక్
                    with page.expect_download() as download_info:
                        # నేరుగా బటన్ మీద క్లిక్ చేయకుండా బటన్ టెక్స్ట్ ఉన్న చోట క్లిక్
                        page.click("button:has-text('Download')")
                    
                    download = download_info.value
                    download.save_as(os.path.join(output_folder, f"removed_{img_name}"))
                    os.remove(img_path)
                    
                    # పేజీ రీసెట్
                    page.goto("https://dewatermark.ai/")
                    page.click("text=Auto Remove 4.0")
                    
            except Exception as e:
                print(f"Error: {e}")
            
            context.close()
        browser.close()

if __name__ == "__main__":
    run_automation()