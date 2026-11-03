# -*- coding: utf-8 -*-
"""
Patch App/template.html with Photoroom API Studio, Google Colab Inpainting ngrok, and Smart Studio Canvas.
Deactivates old slow generator (ai_flux) as requested.
"""
import re

with open('App/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the Engine Selection Block in #photobankGenModal
old_engine_block_start = '<!-- Section: Pilih Mesin Image Generation (Actual Generative AI vs Smart Canvas) -->'
old_engine_block_end = '<!-- Section: Pilihan Slot / Variasi Gambar -->'

start_idx = content.find(old_engine_block_start)
end_idx = content.find(old_engine_block_end)

if start_idx != -1 and end_idx != -1:
    new_engine_block = '''<!-- Section: Pilih Mesin Image Generation (Actual Generative AI vs Smart Canvas) -->
                <div style="background: #ffffff; border: 1.5px solid #10b981; border-radius: 10px; padding: 14px 16px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(16, 185, 129, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: #065f46; margin: 0; display: flex; align-items: center; gap: 8px;">
                            <span>⚙️</span> 1. Pilih Mesin Image Generation:
                        </h4>
                        <span style="font-size: 0.75rem; color: #047857; font-weight: 700; background: #d1fae5; padding: 3px 8px; border-radius: 6px;">
                            Auto Download & Sync ke Folder
                        </span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px;">
                        <!-- Engine 1: Photoroom API Studio (Default) -->
                        <label style="background: #ecfdf5; border: 2px solid #059669; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;" id="labelEnginePhotoroom">
                            <input type="radio" name="genEngineRadio" id="enginePhotoroom" value="photoroom" checked onchange="onSelectGenEngine('photoroom')" style="margin-top: 2px; accent-color: #059669;">
                            <div>
                                <div style="display: flex; align-items: center; gap: 6px;">
                                    <span style="font-weight: 800; font-size: 0.85rem; color: #065f46;">🎨 Photoroom API Studio</span>
                                    <span style="background: #10b981; color: #fff; font-size: 0.65rem; font-weight: 800; padding: 1px 6px; border-radius: 4px;">Rekomendasi</span>
                                </div>
                                <div style="font-size: 0.72rem; color: #047857; margin-top: 3px; line-height: 1.35;">
                                    Hapus background & hasilkan foto studio putih murni #FFFFFF resmi (3.5 dtk). Tajam, presisi, anti-cacat.
                                </div>
                            </div>
                        </label>

                        <!-- Engine 2: Google Colab Diffusers Inpainting -->
                        <label style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;" id="labelEngineColab">
                            <input type="radio" name="genEngineRadio" id="engineColab" value="colab_diffusers" onchange="onSelectGenEngine('colab_diffusers')" style="margin-top: 2px; accent-color: #6366f1;">
                            <div>
                                <div style="display: flex; align-items: center; gap: 6px;">
                                    <span style="font-weight: 800; font-size: 0.85rem; color: #4338ca;">🚀 Google Colab (ngrok GPU T4)</span>
                                    <span style="background: #6366f1; color: #fff; font-size: 0.65rem; font-weight: 800; padding: 1px 6px; border-radius: 4px;">SD Inpainting</span>
                                </div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 3px; line-height: 1.35;">
                                    Stable Diffusion Inpainting via FastAPI + ngrok. Menghasilkan latar lumpur/kebun/pabrik untuk Slot 4.
                                </div>
                            </div>
                        </label>

                        <!-- Engine 3: Studio Smart Canvas -->
                        <label style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;" id="labelEngineOffline">
                            <input type="radio" name="genEngineRadio" id="engineOffline" value="smart_canvas" onchange="onSelectGenEngine('smart_canvas')" style="margin-top: 2px; accent-color: #d97706;">
                            <div>
                                <div style="font-weight: 800; font-size: 0.85rem; color: #d97706;">📐 Studio Smart Canvas (Offline)</div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 3px; line-height: 1.35;">
                                    Auto-crop & scale 85% frame kanvas putih murni #FFFFFF lokal via Python/PIL. 100% instan tanpa internet.
                                </div>
                            </div>
                        </label>

                        <!-- Engine 4: Google AI Studio / Imagen 3 -->
                        <label style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;" id="labelEngineGoogle">
                            <input type="radio" name="genEngineRadio" id="engineGoogle" value="google_ai_studio" onchange="onSelectGenEngine('google_ai_studio')" style="margin-top: 2px; accent-color: #0284c7;">
                            <div>
                                <div style="font-weight: 800; font-size: 0.85rem; color: #0284c7;">🔑 Google AI Studio / Imagen 3</div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 3px; line-height: 1.35;">
                                    Generasi visual AI dengan API Key Google AI Studio pribadi Anda (Imagen 3.0 HD).
                                </div>
                            </div>
                        </label>
                    </div>

                    <!-- Photoroom Key Settings Box -->
                    <div id="photoroomKeyBox" style="margin-top: 12px; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 10px 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
                            <label style="font-size: 0.78rem; font-weight: 800; color: #065f46;">
                                Photoroom API Key:
                            </label>
                            <div style="display: flex; gap: 12px; align-items: center; font-size: 0.72rem;">
                                <label style="display: flex; align-items: center; gap: 4px; cursor: pointer; color: #047857; font-weight: 700;">
                                    <input type="radio" name="prKeyMode" value="pro" checked onchange="switchPrKey('pro')" style="accent-color: #059669;">
                                    Production (Clean No Watermark)
                                </label>
                                <label style="display: flex; align-items: center; gap: 4px; cursor: pointer; color: #64748b;">
                                    <input type="radio" name="prKeyMode" value="sandbox" onchange="switchPrKey('sandbox')" style="accent-color: #059669;">
                                    Sandbox (With Watermark)
                                </label>
                            </div>
                        </div>
                        <input type="text" id="inputPhotoroomKey" value="sk_pr_default_5cf2ec3a5a6ce7e52ab8dcfa7b50d2dbca4dd651" style="width: 100%; padding: 6px 10px; border: 1px solid #6ee7b7; border-radius: 6px; font-size: 0.8rem; font-family: monospace; background: #ffffff;">
                        <div style="font-size: 0.72rem; color: #047857; margin-top: 4px;">
                            ✓ Terhubung ke Photoroom Segment API v1 (Seamless White Studio 1:1, auto crop padding & centering).
                        </div>
                    </div>

                    <!-- Colab ngrok Settings Box -->
                    <div id="colabNgrokBox" style="display: none; margin-top: 12px; background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 8px; padding: 10px 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
                            <label style="font-size: 0.78rem; font-weight: 800; color: #3730a3;">
                                Google Colab Diffusers Inpainting ngrok URL:
                            </label>
                            <div style="display: flex; gap: 8px;">
                                <a href="https://colab.research.google.com/drive/1Vnoy0QT1gzMCPwsif1yheAslk6tUHUv4?usp=sharing" target="_blank" style="font-size: 0.72rem; font-weight: 800; color: #4338ca; text-decoration: underline;">
                                    🚀 Buka Notebook Colab Google Drive ↗
                                </a>
                                <span style="color: #c7d2fe;">|</span>
                                <a href="https://colab.research.google.com/notebook#fileId=https%3A//huggingface.co/stable-diffusion-v1-5/stable-diffusion-inpainting.ipynb" target="_blank" style="font-size: 0.72rem; color: #6366f1; text-decoration: underline;">
                                    🤗 HuggingFace SD Inpaint ↗
                                </a>
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <input type="text" id="inputColabNgrokUrl" placeholder="https://abcd-123.ngrok-free.app/generate-background/" style="flex: 1; padding: 6px 10px; border: 1px solid #a5b4fc; border-radius: 6px; font-size: 0.8rem; font-family: monospace; background: #ffffff;">
                        </div>
                        <div style="font-size: 0.72rem; color: #4338ca; margin-top: 4px;">
                            Jalankan notebook di Google Colab (GPU T4 gratis), lalu salin URL ngrok publik ke kolom di atas.
                        </div>
                    </div>

                    <!-- Google AI Studio Settings Box -->
                    <div id="googleApiKeyBox" style="display: none; margin-top: 12px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 10px 14px;">
                        <label style="font-size: 0.78rem; font-weight: 700; color: #0369a1; display: block; margin-bottom: 4px;">
                            Google AI Studio API Key (<code style="background: rgba(255,255,255,0.7); padding: 1px 4px; border-radius: 3px;">AIzaSy...</code>):
                        </label>
                        <div style="display: flex; gap: 8px;">
                            <input type="password" id="inputGoogleApiKey" oninput="validateGoogleKeyInput(this.value)" placeholder="Paste AIzaSy... key dari aistudio.google.com/app/apikey" style="flex: 1; padding: 6px 10px; border: 1px solid #7dd3fc; border-radius: 6px; font-size: 0.8rem; font-family: monospace;">
                            <a href="https://aistudio.google.com/app/apikey" target="_blank" style="padding: 6px 12px; background: #0284c7; color: #fff; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-decoration: none; display: flex; align-items: center;">
                                Dapatkan Key Gratis ↗
                            </a>
                        </div>
                        <div id="googleKeyWarning" style="display: none; margin-top: 8px; font-size: 0.74rem; color: #b91c1c; background: #fef2f2; border: 1px solid #fecaca; padding: 8px 12px; border-radius: 6px; line-height: 1.45;">
                            ⚠️ <strong>Pemberitahuan Token:</strong> Token berawalan <code>AQ...</code> adalah token internal sesi editor, bukan API Key Google AI Studio. Google AI Studio selalu berawalan <code>AIzaSy...</code>.
                        </div>
                    </div>
                </div>

                '''
    content = content[:start_idx] + new_engine_block + content[end_idx:]
    print("Replaced Engine Selection HTML successfully!")
else:
    print("WARNING: Could not find engine block indices!")

# 2. Update onSelectGenEngine and add switchPrKey
old_onselect = '''        function onSelectGenEngine(engine) {
            const lFlux = document.getElementById('labelEngineFlux');
            const lG = document.getElementById('labelEngineGoogle');
            const lOff = document.getElementById('labelEngineOffline');
            if (lFlux) {
                lFlux.style.borderColor = engine === 'ai_flux' ? '#059669' : '#cbd5e1';
                lFlux.style.background = engine === 'ai_flux' ? '#ecfdf5' : '#f8fafc';
            }
            if (lG) {
                lG.style.borderColor = engine === 'google_ai_studio' ? '#0284c7' : '#cbd5e1';
                lG.style.background = engine === 'google_ai_studio' ? '#f0f9ff' : '#f8fafc';
            }
            if (lOff) {
                lOff.style.borderColor = engine === 'offline_canvas' ? '#d97706' : '#cbd5e1';
                lOff.style.background = engine === 'offline_canvas' ? '#fffbeb' : '#f8fafc';
            }
            const apiKeyBox = document.getElementById('googleApiKeyBox');
            if (apiKeyBox) {
                apiKeyBox.style.display = engine === 'google_ai_studio' ? 'block' : 'none';
            }
        }'''

new_onselect = '''        function onSelectGenEngine(engine) {
            const lPR = document.getElementById('labelEnginePhotoroom');
            const lColab = document.getElementById('labelEngineColab');
            const lG = document.getElementById('labelEngineGoogle');
            const lOff = document.getElementById('labelEngineOffline');
            
            if (lPR) {
                lPR.style.borderColor = engine === 'photoroom' ? '#059669' : '#cbd5e1';
                lPR.style.background = engine === 'photoroom' ? '#ecfdf5' : '#f8fafc';
            }
            if (lColab) {
                lColab.style.borderColor = engine === 'colab_diffusers' ? '#6366f1' : '#cbd5e1';
                lColab.style.background = engine === 'colab_diffusers' ? '#eef2ff' : '#f8fafc';
            }
            if (lG) {
                lG.style.borderColor = engine === 'google_ai_studio' ? '#0284c7' : '#cbd5e1';
                lG.style.background = engine === 'google_ai_studio' ? '#f0f9ff' : '#f8fafc';
            }
            if (lOff) {
                lOff.style.borderColor = (engine === 'smart_canvas' || engine === 'offline_canvas') ? '#d97706' : '#cbd5e1';
                lOff.style.background = (engine === 'smart_canvas' || engine === 'offline_canvas') ? '#fffbeb' : '#f8fafc';
            }
            
            const prBox = document.getElementById('photoroomKeyBox');
            if (prBox) prBox.style.display = engine === 'photoroom' ? 'block' : 'none';

            const colabBox = document.getElementById('colabNgrokBox');
            if (colabBox) colabBox.style.display = engine === 'colab_diffusers' ? 'block' : 'none';

            const gBox = document.getElementById('googleApiKeyBox');
            if (gBox) gBox.style.display = engine === 'google_ai_studio' ? 'block' : 'none';
        }

        function switchPrKey(mode) {
            const inp = document.getElementById('inputPhotoroomKey');
            if (!inp) return;
            if (mode === 'pro') {
                inp.value = 'sk_pr_default_5cf2ec3a5a6ce7e52ab8dcfa7b50d2dbca4dd651';
            } else {
                inp.value = 'sandbox_sk_pr_default_5cf2ec3a5a6ce7e52ab8dcfa7b50d2dbca4dd651';
            }
        }
        window.switchPrKey = switchPrKey;'''

if old_onselect in content:
    content = content.replace(old_onselect, new_onselect, 1)
    print("Replaced onSelectGenEngine successfully!")
else:
    print("WARNING: Could not find old onSelectGenEngine block!")

# 3. Update executeCustomPhotobankGeneration to read engine, Photoroom key, and ngrok URL
old_fetch_custom = '''            const engineRadio = document.querySelector('input[name="genEngineRadio"]:checked');
            const selectedEngine = engineRadio ? engineRadio.value : 'ai_flux';
            const googleApiKey = document.getElementById('inputGoogleApiKey') ? document.getElementById('inputGoogleApiKey').value.trim() : '';'''

new_fetch_custom = '''            const engineRadio = document.querySelector('input[name="genEngineRadio"]:checked');
            const selectedEngine = engineRadio ? engineRadio.value : 'photoroom';
            let apiKeyToUse = '';
            if (selectedEngine === 'photoroom') {
                const prKeyInput = document.getElementById('inputPhotoroomKey');
                apiKeyToUse = prKeyInput ? prKeyInput.value.trim() : 'sk_pr_default_5cf2ec3a5a6ce7e52ab8dcfa7b50d2dbca4dd651';
            } else if (selectedEngine === 'google_ai_studio') {
                const gKeyInput = document.getElementById('inputGoogleApiKey');
                apiKeyToUse = gKeyInput ? gKeyInput.value.trim() : '';
            }
            const ngrokUrlInput = document.getElementById('inputColabNgrokUrl');
            const ngrokUrl = ngrokUrlInput ? ngrokUrlInput.value.trim() : '';'''

if old_fetch_custom in content:
    content = content.replace(old_fetch_custom, new_fetch_custom, 1)
    print("Replaced custom gen engine parameter extraction successfully!")
else:
    print("WARNING: Could not find old_fetch_custom block!")

# Also replace the fetch body inside loop
old_body = '''                        body: JSON.stringify({
                            sku: item.sku,
                            folder: item.folder,
                            slots: slots,
                            target_size: targetSize,
                            fill_ratio: fillRatio,
                            save_to_shopee: saveShopee,
                            save_to_flow: saveFlow,
                            save_to_photobank: savePhotobank,
                            engine: selectedEngine,
                            api_key: googleApiKey
                        })'''

new_body = '''                        body: JSON.stringify({
                            sku: item.sku,
                            folder: item.folder,
                            slots: slots,
                            target_size: targetSize,
                            fill_ratio: fillRatio,
                            save_to_shopee: saveShopee,
                            save_to_flow: saveFlow,
                            save_to_photobank: savePhotobank,
                            engine: selectedEngine,
                            api_key: apiKeyToUse,
                            ngrok_url: ngrokUrl
                        })'''

if old_body in content:
    content = content.replace(old_body, new_body, 1)
    print("Replaced fetch body successfully!")
else:
    print("WARNING: Could not find old_body block!")

with open('App/template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("App/template.html successfully updated!")

