from playwright.sync_api import sync_playwright
import os
import time
import base64

last_downloaded_id = None

def download_image(page, save_folder="downloaded_images"):
    global last_downloaded_id
    if not os.path.exists(save_folder): os.makedirs(save_folder)
    
    try:
        # మెసేజ్ కంటెంట్ లోపల ఉన్న ఇమేజ్‌లను మాత్రమే వెతకండి
        all_imgs = page.locator("message-content img[src^='blob:']")
        count = all_imgs.count()
        
        for i in range(count):
            target_img = all_imgs.nth(i)
            img_src = target_img.get_attribute("src")
            
            # ఇమేజ్ సైజు చెక్ (చాలా చిన్న ఐకాన్స్ వదిలేయడానికి)
            box = target_img.bounding_box()
            if not box or box['width'] < 150:
                continue
                
            if img_src == last_downloaded_id:
                continue

            # Canvas ద్వారా ఇమేజ్ డేటాను పొందండి
            js_code = """
            (src) => {
                const img = document.querySelector('img[src="' + src + '"]');
                const canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                return canvas.toDataURL('image/png');
            }
            """
            base64_data = page.evaluate(js_code, img_src)
            
            file_name = f"gemini_ai_{int(time.time())}.png"
            save_path = os.path.join(save_folder, file_name)
            
            if "," in base64_data:
                base64_data = base64_data.split(",", 1)[1]
                
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(base64_data))
                
            last_downloaded_id = img_src
            print(f"\n--- [SUCCESS] AI ఇమేజ్ డౌన్‌లోడ్ అయ్యింది: {file_name} ---")
                
    except Exception as e:
        print(f"\n--- [ERROR] డౌన్‌లోడ్ ఫెయిల్ అయ్యింది: {e} ---")

def run_chat_bot():
    user_data_dir = "./user_data"
    if not os.path.exists(user_data_dir): os.makedirs(user_data_dir)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir, channel='msedge', headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0]
        page.goto("https://gemini.google.com")
        time.sleep(5)
        
        print("\n--- [Gemini Bot Active] ---")
        
        while True:
            user_input = input("\nమీరు (exit కొడితే ఆగిపోతుంది): ")
            if user_input.lower() == "exit": break

            if user_input.lower().startswith("upload "):
                file_paths = [f.strip().replace('"', '') for f in user_input.split(" ", 1)[1].split(",")]
                page.click("button[aria-label='Upload and tools']")
                with page.expect_file_chooser() as fc_info:
                    page.get_by_text("Upload files").click()
                fc_info.value.set_files([os.path.abspath(f) for f in file_paths if os.path.exists(f)])
                time.sleep(4)
                continue
            
            chat_box = page.locator("div.ql-editor.textarea")
            chat_box.click()
            chat_box.fill("")
            chat_box.type(user_input, delay=10)
            page.keyboard.press("Enter")
            
            print("Gemini: ", end="", flush=True)
            last_msg_text = ""
            
            # రెస్పాన్స్ వచ్చే వరకు వెయిట్ చేయడం
            while True:
                time.sleep(0.5)
                # స్టాప్ బటన్ లేదంటే రెస్పాన్స్ కంప్లీట్ అయినట్లు
                if page.locator("mat-icon[fonticon='stop']").count() == 0:
                    break
            
            # కంప్లీట్ అయిన తర్వాత డౌన్‌లోడ్ ఫంక్షన్ ని ఒక్కసారి రన్ చేయండి
            time.sleep(2)
            download_image(page)
            print("\n")
        
        context.close()

if __name__ == "__main__":
    run_chat_bot()